class PacmanPkgInfo():
    """Class that contains package information extracted from the given alpm package object, with additional package manager specifics."""
    def __init__(self, alpm_pkginfo, marked: bool, installed: bool, repo: str) -> None:
        self.marked = marked
        self.installed = installed
        self.repo = repo
        self.name = alpm_pkginfo.name
        self.version = alpm_pkginfo.version
        self.size = alpm_pkginfo.size
        self.isize = alpm_pkginfo.isize
        self.desc = alpm_pkginfo.desc
        self.url = alpm_pkginfo.url
        self.licenses = alpm_pkginfo.licenses
        self.builddate = alpm_pkginfo.builddate
        self.depends = alpm_pkginfo.depends
        self.optdepends = alpm_pkginfo.optdepends
        self.groups = alpm_pkginfo.groups

class SystemdServiceInfo():
    """Class that contains systemd service information."""
    def __init__(self, unitname, desc, servicestate, runstate) -> None:
        self.unitname = unitname
        self.desc = desc
        self.servicestate = servicestate
        self.runstate = runstate
