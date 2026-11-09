import os, platform, shutil, stat, tarfile, urllib.request

def install_bin(url, name, install_dir):
    os.makedirs(install_dir, exist_ok=True)
    target = os.path.join(install_dir, name)
    print(f"Downloading {name} from {url}")
    urllib.request.urlretrieve(url, target)
    os.chmod(target, 0o755)
    return target

def install_oras_tarball(url, install_dir):
    arch = "arm64" if platform.machine() in ("aarch64", "arm64") else "amd64"
    tgz = f"/tmp/oras_{arch}.tar.gz"
    urllib.request.urlretrieve(url, tgz)
    with tarfile.open(tgz) as t:
        t.extract("oras", path="/tmp")
    target = os.path.join(install_dir, "oras")
    shutil.move("/tmp/oras", target)
    os.chmod(target, 0o755)
    return target

def main():
    arch = "arm64" if platform.machine() in ("aarch64", "arm64") else "amd64"
    install_dir = "/usr/local/bin"
    if not os.access(install_dir, os.W_OK):
        install_dir = os.path.expanduser("~/.local/bin")

    sops_v = os.environ["SOPS_VERSION"]
    sops = install_bin(
        f"https://github.com/getsops/sops/releases/download/v{sops_v}/sops-v{sops_v}.linux.{arch}",
        "sops",
        install_dir
    )

    oras_v = os.environ["ORAS_VERSION"]
    oras = install_oras_tarball(
        f"https://github.com/oras-project/oras/releases/download/v{oras_v}/oras_{oras_v}_linux_{arch}.tar.gz",
        install_dir
    )

    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"sops-path={sops}\n")
        f.write(f"oras-path={oras}\n")
    with open(os.environ["GITHUB_PATH"], "a") as f:
        f.write(install_dir + "\n")

    print(f"Installed sops={sops}, oras={oras}")


if __name__ == "__main__":
    main()