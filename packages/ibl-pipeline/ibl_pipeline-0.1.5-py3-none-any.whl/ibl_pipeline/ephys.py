import datajoint as dj
import numpy as np
from os import path, environ
from . import acquisition, reference, behavior, data
from tqdm import tqdm
import numpy as np
from uuid import UUID
import re
import alf.io

try:
    from oneibl.one import ONE
    one = ONE()
except:
    print('ONE not set up')

mode = environ.get('MODE')

if mode == 'update':
    schema = dj.schema('ibl_ephys')
else:
    schema = dj.schema(dj.config.get('database.prefix', '') + 'ibl_ephys')

dj.config['safemode'] = False


@schema
class Probe(dj.Lookup):
    definition = """
    # Description of a particular model of probe
    probe_model_name:       varchar(128)        # String naming probe model, from probe.description
    probe_serial_number:    varchar(64)         # serial number of a probe
    ---
    channel_counts:         smallint            # number of channels in the probe
    """

    class Channel(dj.Part):
        definition = """
        # positional information about every channel on this probe
        -> master
        channel_id:     smallint         # id of a channel on the probe
        ---
        channel_x_pos=null:  float       # x position relative to the tip of the probe in um, on the width of the shank
        channel_y_pos=null:  float       # y position relative to the tip of the probe in um, the depth where 0 is the deepest site, and positive above this
        channel_shank=null:  tinyint     # shank of the channel, 1 or 2
        """


@schema
class CompleteClusterSession(dj.Computed):
    definition = """
    # sessions that are complete with ephys datasets
    -> acquisition.Session
    ---
    complete_cluster_session=CURRENT_TIMESTAMP  :  timestamp
    """
    required_datasets = [
        'clusters.amps.npy',
        'clusters.channels.npy',
        'clusters.depths.npy',
        'metrics.csv',
        'clusters.peakToTrough.npy',
        'clusters.uuids.csv',
        'clusters.waveforms.npy',
        'clusters.waveformsChannels.npy',
        'spikes.amps.npy',
        'spikes.clusters.npy',
        'spikes.depths.npy',
        'spikes.samples.npy',
        'spikes.templates.npy',
        'spikes.times.npy'
    ]
    key_source = acquisition.Session & \
        'task_protocol like "%ephysChoiceWorld%"' \
        & (data.FileRecord & 'dataset_name="spikes.times.npy"') \
        & (data.FileRecord & 'dataset_name="spikes.clusters.npy"') \
        & (data.FileRecord & 'dataset_name="probes.description.json"')

    def make(self, key):
        datasets = (data.FileRecord & key & 'repo_name LIKE "flatiron_%"' &
                    {'exists': 1}).fetch('dataset_name')
        is_complete = bool(np.all([req_ds in datasets
                                   for req_ds in self.required_datasets]))
        if is_complete:
            self.insert1(key)
            (EphysMissingDataLog & key).delete()
        else:
            for req_ds in self.required_datasets:
                if req_ds not in datasets:
                    EphysMissingDataLog.insert1(
                        dict(**key,
                             missing_data=req_ds),
                        skip_duplicates=True)


@schema
class EphysMissingDataLog(dj.Manual):
    definition = """
    # Keep record of the missing data
    -> acquisition.Session
    missing_data: varchar(255)
    ---
    missing_data_ts=CURRENT_TIMESTAMP:   timestamp
    """


@schema
class ProbeInsertion(dj.Imported):
    definition = """
    -> acquisition.Session
    probe_idx:    int    # probe insertion number (0 corresponds to probe00, 1 corresponds to probe01)
    ---
    -> Probe
    """
    key_source = CompleteClusterSession

    def make(self, key):
        eID = str((acquisition.Session & key).fetch1('session_uuid'))
        dtypes = ['probes.description']
        files = one.load(eID, dataset_types=dtypes, download_only=True)
        ses_path = alf.io.get_session_path(files[0])
        probes = alf.io.load_object(ses_path.joinpath('alf'), 'probes')
        for p in probes['description']:
            # ingest probe information, including probe model and serial
            probe = dict(
                probe_model_name=p['model'],
                probe_serial_number=str(p['serial']),
                channel_counts=960)
            Probe.insert1(probe, skip_duplicates=True)

            # ingest probe insertion
            idx = int(re.search('probe0([0-3])', p['label']).group(1))
            key.update(probe_idx=idx,
                       probe_model_name=p['model'],
                       probe_serial_number=str(p['serial']))
            self.insert1(key)


@schema
class ChannelGroup(dj.Imported):
    definition = """
    -> ProbeInsertion
    ---
    channel_raw_inds:             blob  # Array of integers saying which index in the raw recording file (of its home probe) that the channel corresponds to (counting from zero)
    channel_local_coordinates:    blob  # Location of each channel relative to probe coordinate system (µm): x (first) dimension is on the width of the shank; (y) is the depth where 0 is the deepest site, and positive above this
    """

    key_source = ProbeInsertion \
        & (data.FileRecord & 'dataset_name="channels.rawInd.npy"') \
        & (data.FileRecord & 'dataset_name="channels.localCoordinates.npy"')

    def make(self, key):

        eID = str((acquisition.Session & key).fetch1('session_uuid'))
        dtypes = [
            'channels.rawInd',
            'channels.localCoordinates'
        ]

        files = one.load(eID, dataset_types=dtypes, download_only=True)
        ses_path = alf.io.get_session_path(files[0])

        probe_name = 'probe0' + str(key['probe_idx'])
        channels = alf.io.load_object(
            ses_path.joinpath('alf', probe_name), 'channels')

        self.insert1(
            dict(**key,
                 channel_raw_inds=channels.rawInd,
                 channel_local_coordinates=channels.localCoordinates))


@schema
class ProbeTrajectory(dj.Imported):
    definition = """
    # data imported from probes.trajectory
    -> ProbeInsertion
    ---
    x:                  float           # (um) medio-lateral coordinate relative to Bregma, left negative
    y:                  float           # (um) antero-posterior coordinate relative to Bregma, back negative
    z:                  float           # (um) dorso-ventral coordinate relative to Bregma, ventral negative
    phi:                float           # (degrees)[-180 180] azimuth
    theta:              float           # (degrees)[0 180] polar angle
    depth:              float           # (um) insertion depth
    beta:               float           # (degrees) roll angle of the probe
    """
    key_source = acquisition.Session \
        & (data.FileRecord & 'dataset_name="probes.description.json"') \
        & (data.FileRecord & 'dataset_name="probes.trajectory.json"')

    def make(self, key):
        eID = str((acquisition.Session & key).fetch1('session_uuid'))
        dtypes = ['probes.description', 'probes.trajectory']
        files = one.load(eID, dataset_types=dtypes, download_only=True)
        ses_path = alf.io.get_session_path(files[0])
        probes = alf.io.load_object(ses_path.joinpath('alf'), 'probes')
        for p in probes.trajectory:

            # ingest probe trajectory
            idx = int(re.search('probe0([0-3])', p['label']).group(1))
            p.pop('label')
            key.update(probe_idx=idx, **p)
            self.insert1(key)


# needs to be further adjusted by adding channels.mlapdvIntended
@schema
class ChannelBrainLocation(dj.Imported):
    definition = """
    -> ProbeInsertion
    -> Probe.Channel
    -> reference.Atlas
    histology_revision: varchar(64)
    ---
    # from channels.brainlocation
    version_time:       datetime
    channel_ap:         float           # anterior posterior CCF coordinate (um)
    channel_dv:         float           # dorsal ventral CCF coordinate (um)
    channel_lr:         float           # left right CCF coordinate (um)
    -> reference.BrainLocationAcronym.proj(channel_brain_location='acronym')   # acronym of the brain location
    channel_raw_row:        smallint    # Each channel's row in its home file (look up via probes.rawFileName), counting from zero. Note some rows don't have a channel, for example if they were sync pulses
    """


@schema
class Cluster(dj.Imported):
    definition = """
    -> ProbeInsertion
    cluster_revision='0':            varchar(64)
    cluster_id:                      int
    ---
    cluster_uuid:                    uuid            # uuid of this cluster
    cluster_channel:                 int             # which channel this cluster is from
    cluster_amp=null:                float           # Mean amplitude of each cluster (µV)
    cluster_waveforms=null:          blob@ephys      # Waveform from spike sorting templates (stored as a sparse array, only for a subset of channels closest to the peak channel)
    cluster_waveforms_channels=null: blob@ephys      # Index of channels that are stored for each cluster waveform. Sorted by increasing distance from the maximum amplitude channel.
    cluster_depth=null:              float           # Depth of mean cluster waveform on probe (µm). 0 means deepest site, positive means above this.
    cluster_peak_to_trough=null:     blob@ephys      # trough to peak time (ms)
    cluster_spikes_times:            blob@ephys      # spike times of a particular cluster (seconds)
    cluster_spikes_depths:           blob@ephys      # Depth along probe of each spike (µm; computed from waveform center of mass). 0 means deepest site, positive means above this
    cluster_spikes_amps:             blob@ephys      # Amplitude of each spike (µV)
    cluster_spikes_templates=null:   blob@ephys      # Template ID of each spike (i.e. output of automatic spike sorting prior to manual curation)
    cluster_spikes_samples=null:     blob@ephys      # Time of spikes, measured in units of samples in their own electrophysiology binary file.
    """
    key_source = ProbeInsertion

    def make(self, key):
        eID = str((acquisition.Session & key).fetch1('session_uuid'))

        dtypes = [
            'clusters.amps',
            'clusters.channels',
            'clusters.depths',
            'clusters.metrics',
            'clusters.peakToTrough',
            'clusters.uuids',
            'clusters.waveforms',
            'clusters.waveformsChannels',
            'spikes.amps',
            'spikes.clusters',
            'spikes.depths',
            'spikes.samples',
            'spikes.templates',
            'spikes.times'
        ]

        files = one.load(eID, dataset_types=dtypes, download_only=True)
        ses_path = alf.io.get_session_path(files[0])

        probe_name = 'probe0' + str(key['probe_idx'])

        clusters = alf.io.load_object(
            ses_path.joinpath('alf', probe_name), 'clusters')
        spikes = alf.io.load_object(
            ses_path.joinpath('alf', probe_name), 'spikes')

        for icluster, cluster_uuid in tqdm(enumerate(clusters.uuids['uuids'])):

            idx = spikes.clusters == icluster
            cluster = dict(
                **key,
                cluster_id=icluster,
                cluster_uuid=cluster_uuid,
                cluster_channel=clusters.channels[icluster],
                cluster_amp=clusters.amps[icluster],
                cluster_waveforms=clusters.waveforms[icluster],
                cluster_waveforms_channels=clusters.waveformsChannels[icluster],
                cluster_depth=clusters.depths[icluster],
                cluster_peak_to_trough=clusters.peakToTrough[icluster],
                cluster_spikes_times=spikes.times[idx],
                cluster_spikes_depths=spikes.depths[idx],
                cluster_spikes_amps=spikes.amps[idx],
                cluster_spikes_templates=spikes.templates[idx],
                cluster_spikes_samples=spikes.samples[idx])

            self.insert1(cluster)

            metrics = clusters.metrics
            cluster_metric_entry = dict(
                **key,
                cluster_id=icluster,
                cluster_revision='0',
                num_spikes=metrics.num_spikes[icluster],
                firing_rate=metrics.firing_rate[icluster],
                presence_ratio=metrics.presence_ratio[icluster],
                presence_ratio_std=metrics.presence_ratio_std[icluster],
                amplitude_cutoff=metrics.amplitude_cutoff[icluster],
                amplitude_std=metrics.amplitude_std[icluster],
                epoch_name=metrics.epoch_name[icluster],
                ks2_contamination_pct=metrics.ks2_contamination_pct[icluster],
                ks2_label=metrics.ks2_label[icluster])

            if not np.isnan(metrics.isi_viol[icluster]):
                cluster_metric_entry.update(
                    isi_viol=metrics.isi_viol[icluster])

            self.ClusterMetrics.insert1(cluster_metric_entry)

    class ClusterMetrics(dj.Part):
        definition = """
        -> master
        ---
        num_spikes:                 int    # total spike number
        firing_rate:                float  # firing rate of the cluster
        presence_ratio=null:        float
        presence_ratio_std=null:    float
        isi_viol=null:              float
        amplitude_cutoff=null:      float
        amplitude_std=null:         float
        epoch_name:                 tinyint
        ks2_contamination_pct:      float
        ks2_label:                  enum('good', 'mua')
        """


@schema
class ClusterBrainLocation(dj.Imported):
    definition = """
    -> Cluster
    ---
    -> reference.BrainLocationAcronym    # acronym of the brain location
    cluster_ml_position:      float      # Estimated 3d location of the cell relative to bregma - mediolateral
    cluster_ap_position:      float      # anterior-posterior
    cluster_dv_position:      float      # dorsoventral
    """


@schema
class Event(dj.Lookup):
    definition = """
    event:       varchar(32)
    """
    contents = zip(['go cue', 'stim on', 'response', 'feedback'])


@schema
class TrialSpikes(dj.Computed):
    definition = """
    -> Cluster
    -> behavior.TrialSet.Trial
    -> Event
    ---
    trial_spike_times=null:   longblob     # spike time for each trial, aligned to different event times
    """
    key_source = behavior.TrialSet * Cluster

    def make(self, key):
        trials = behavior.TrialSet.Trial & key
        trial_spks = []
        cluster = Cluster() & key
        spike_times = cluster.fetch1('cluster_spikes_times')

        for trial, itrial in tqdm(zip(trials.fetch(as_dict=True), trials.fetch('KEY'))):
            trial_spk = dict(
                **itrial,
                cluster_id=key['cluster_id'],
                cluster_revision=key['cluster_revision'],
                probe_idx=key['probe_idx']
            )
            f = np.logical_and(spike_times < trial['trial_end_time'],
                               spike_times > trial['trial_start_time'])

            events = (Event & 'event!="go cue"').fetch('event')
            for event in events:
                if not np.any(f):
                    trial_spk['trial_spike_times'] = []
                else:
                    if event == 'stim on':
                        trial_spk['trial_spike_times'] = \
                            spike_times[f] - trial['trial_stim_on_time']
                    elif event == 'response':
                        trial_spk['trial_spike_times'] = \
                            spike_times[f] - trial['trial_response_time']
                    elif event == 'feedback':
                        if trial['trial_feedback_time']:
                            trial_spk['trial_spike_times'] = \
                                spike_times[f] - trial['trial_feedback_time']
                        else:
                            continue
                trial_spk['event'] = event
                trial_spks.append(trial_spk.copy())

        self.insert(trial_spks)


@schema
class LFP(dj.Imported):
    definition = """
    -> ProbeInsertion
    ---
    lfp_timestamps:       blob@ephys    # Timestamps for LFP timeseries in seconds
    lfp_start_time:       float         # (seconds)
    lfp_end_time:         float         # (seconds)
    lfp_duration:         float         # (seconds)
    lfp_sampling_rate:    float         # samples per second
    """

    class Channel(dj.Part):
        definition = """
        -> master
        -> Probe.Channel
        ---
        lfp: blob@ephys           # recorded lfp on this channel
        """
