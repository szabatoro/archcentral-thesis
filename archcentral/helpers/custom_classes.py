class PacmanPkgInfo():
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
        self.packager = alpm_pkginfo.packager
        self.builddate = alpm_pkginfo.builddate
        self.files = alpm_pkginfo.files
        self.depends = alpm_pkginfo.depends
