---
task_categories:
- text-generation
language:
  - en
pretty_name: Coats Privacy Policy Dataset
configs:
- config_name: full
  data_files:
  - split: train
    path: data/full/train*
- config_name: behavioral-marketing
  data_files:
  - split: train
    path: data/behavioral-marketing/train*
  - split: test
    path: data/behavioral-marketing/test*
- config_name: security
  data_files:
  - split: train
    path: data/security/train*
  - split: test
    path: data/security/test*    
- config_name: third-party-collection
  data_files:
    - split: train
      path: data/third-party-collection/train*
    - split: test
      path: data/third-party-collection/test*
- config_name: history
  data_files:
    - split: train
      path: data/history/train*
    - split: test
      path: data/history/test*
- config_name: data-deletion
  data_files:
    - split: train
      path: data/data-deletion/train*
    - split: test
      path: data/data-deletion/test*
- config_name: data-breaches
  data_files:
    - split: train
      path: data/data-breaches/train*
    - split: test
      path: data/data-breaches/test*
- config_name: third-party-access
  data_files:
    - split: train
      path: data/third-party-access/train*
    - split: test
      path: data/third-party-access/test*
- config_name: data-collection-reasoning
  data_files:
    - split: train
      path: data/data-collection-reasoning/train*
    - split: test
      path: data/data-collection-reasoning/test*
- config_name: noncritical-purposes
  data_files:
    - split: train
      path: data/noncritical-purposes/train*
    - split: test
      path: data/noncritical-purposes/test*
- config_name: law-enforcement
  data_files:
    - split: train
      path: data/law-enforcement/train*
    - split: test
      path: data/law-enforcement/test*
- config_name: list-collected
  data_files:
    - split: train
      path: data/list-collected/train*
    - split: test
      path: data/list-collected/test*
- config_name: revision-notify
  data_files:
    - split: train
      path: data/revision-notify/train*
    - split: test
      path: data/revision-notify/test*
---
