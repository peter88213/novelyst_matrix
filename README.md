# novelyst_matrix

A plugin providing a scene relationship matrix. 

For more information, see the [project homepage](https://peter88213.github.io/novelyst_matrix) with description and download instructions.


## Development

*novelyst_matrix* depends on the [pywriter](https://github.com/peter88213/PyWriter) and the [yw-table](https://github.com/peter88213/yw-table) libraries which must be present in your file system. It is organized as an Eclipse PyDev project. The official release branch on GitHub is *main*.

### Mandatory directory structure for building the application script

```
.
├── PyWriter/
│   └── src/
│       └── pywriter/
├── yw-table/
│   └── src/
│      └── ywtablelib/
└── novelyst_matrix/
    ├── src/
    ├── test/
    └── tools/ 
        └── build.xml
```

### Conventions

- Minimum Python version is 3.6. 
- The Python **source code formatting** follows widely the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide, except the maximum line length, which is 120 characters here.

### Development tools

- [Python](https://python.org) version 3.11
- [Eclipse IDE](https://eclipse.org) with [PyDev](https://pydev.org) and [EGit](https://www.eclipse.org/egit/)
- [Apache Ant](https://ant.apache.org/) for building the application script


## License

This is Open Source software, and the *novelyst_matrix* plugin is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelyst_matrix/blob/main/LICENSE) file.
