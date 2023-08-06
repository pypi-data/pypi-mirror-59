# ndx-labmetadata-giocomo extension for NWB:N

Extension of the [lab_meta_data](https://pynwb.readthedocs.io/en/stable/pynwb.file.html#pynwb.file.NWBFile.lab_meta_data) field.
A collaboration with [Giocomo Lab](https://giocomolab.weebly.com/).

[![PyPI version]()

[Python Installation](#python-installation)

[Python Usage](#python-usage)

### Python Installation
```bash
pip install git+https://github.com/ben-dichter-consulting/ndx-labmetadata-giocomo.git
```

### Python Usage

```python
from datetime import datetime
from pynwb import NWBFile, NWBHDF5IO
from ndx_labmetadata_giocomo import LabMetaData_ext

nwb = NWBFile('session_description', 'identifier', datetime.now().astimezone())

# Creates LabMetaData container
lab_metadata = LabMetaData_ext(
    name='LabMetaData',
    acquisition_sampling_rate=1000.,
    number_of_electrodes=10,
    file_path='',
    bytes_to_skip=2,
    raw_data_dtype='int16',
    high_pass_filtered=False,
    movie_start_time=13.6,
    subject_brain_region='Medial Entorhinal Cortex'
)

# Add to file
nwb.add_lab_meta_data(lab_metadata)

# Write nwb file
with NWBHDF5IO('test_labmetadata.nwb', 'w') as io:
    io.write(nwb)

# Read nwb file and check its content
with NWBHDF5IO('test_labmetadata.nwb', 'r', load_namespaces=True) as io:
    nwb = io.read()
    print(nwb.lab_meta_data['LabMetaData'])
```
