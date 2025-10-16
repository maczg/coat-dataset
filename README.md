---
configs:
- config_name: full
  data_files:
  - split: train
    path: full/train*
- config_name: behavioral-marketing
  data_files:
  - split: train
    path: behavioral-marketing/train*
  - split: test
    path: behavioral-marketing/test*
- config_name: security
  data_files:
  - split: train
    path: security/train*
- config_name: third-party-collection
  data_files:
    - split: train
      path: third-party-collection/train*
    - split: test
      path: third-party-collection/test*
- config_name: history
  data_files:
    - split: train
      path: history/train*
    - split: test
      path: history/test*
- config_name: data-deletion
  data_files:
    - split: train
      path: data-deletion/train*
    - split: test
      path: data-deletion/test*
- config_name: data-breaches
  data_files:
    - split: train
      path: data-breaches/train*
    - split: test
      path: data-breaches/test*
- config_name: third-party-access
  data_files:
    - split: train
      path: third-party-access/train*
    - split: test
      path: third-party-access/test*
- config_name: data-collection-reasoning
  data_files:
    - split: train
      path: data-collection-reasoning/train*
    - split: test
      path: data-collection-reasoning/test*
- config_name: noncritical-purposes
  data_files:
    - split: train
      path: noncritical-purposes/train*
    - split: test
      path: noncritical-purposes/test*
- config_name: law-enforcement
  data_files:
    - split: train
      path: law-enforcement/train*
    - split: test
      path: law-enforcement/test*
- config_name: list-collected
  data_files:
    - split: train
      path: list-collected/train*
    - split: test
      path: list-collected/test*
- config_name: revision-notify
  data_files:
    - split: train
      path: revision-notify/train*
    - split: test
      path: revision-notify/test*
---
