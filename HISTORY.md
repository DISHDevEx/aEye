Release History
===============

1.2.4
---
- Bug fix in Aux.clean()
    - Added exception handling and changed implementation to ```shutil.rmtree(path)```

1.1.0 Additional Features
---

- Update README.md
- Added change_fps in Labeler
- Added set_bitrate in Labeler
- Added greyscale in Labeler 
- Removed Deprecated Code
- Temporary folders are now created when executing label, rather than instantiating Aux, reducing the amount of unneeded directories

1.0.0 Initial Release
---

- Initial release for framework
- Video Labeling functionality
- Frame Extraction
