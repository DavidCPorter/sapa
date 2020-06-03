
module : cloud-env

=========

This installs the machines the infrastructure will deploy to. 


Requirements
------------
- ubuntu18 LTS running on every server. 

- You will need to have a complete inventory with required groups and formatting per janus specification. 


Module Variables
--------------
Please use UI for variable assignment, however, these are the vars in this module:
```
vars:
    ramdisk_path: /dev/shm
    ptp_install_dir: '/users/{{ansible_user}}/linuxptp'
    cred_dir: "{{JANUS_HOME}}/playbooks/roles/cloud-env/files/.aws"
    rem_user: dporte7
    packages:
      - awscli
      - python3-pip
      - python3-dev
      - htop
      - dstat
      - maven
      - ant
      - virtualenv #required for pip
    # - setuptools #required for pip
```


License
-------

BSD

Author Information
------------------

David Porter 
dporte7@uic.edu

