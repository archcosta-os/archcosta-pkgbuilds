#!/bin/bash

# ArchCosta Universal Repository Builder
# Works on Arch Linux (native) and Ubuntu (via Docker)

# Configuration
MAIN_DIR=$(cd ../ && pwd)
REPO_DIR="$MAIN_DIR/local-repo"
CONTAINER_IMAGE="archlinux:latest"

echo "--------------------------------------------------"
echo "🚀 ArchCosta Repo Build Starting..."
echo "Environment: $(lsb_release -ds 2>/dev/null || echo "Arch Linux")"
echo "--------------------------------------------------"

# Function: Build package natively (Arch Linux)
build_native() {
    echo ":: Building natively on Arch Linux..."
    # 1. Cleanup
    find . -maxdepth 2 -name "src" -type d -exec rm -rf {} +
    find . -maxdepth 2 -name "pkg" -type d -exec rm -rf {} +
    rm -rf "$REPO_DIR" && mkdir -p "$REPO_DIR"

    # 2. Build loop
    for pkg in */; do
        if [ -d "$pkg" ] && [ -f "$pkg/PKGBUILD" ]; then
            echo ":: Processing $pkg"
            (cd "$pkg" && makepkg -scfd --noconfirm)
        fi
    done

    # 3. Gather and Generate DB
    find . -name "*.pkg.tar.zst" -exec cp -f {} "$REPO_DIR/" \;
    cd "$REPO_DIR"
    repo-add archcosta.db.tar.gz *.pkg.tar.zst
    ln -sf archcosta.db.tar.gz archcosta.db
    ln -sf archcosta.files.tar.gz archcosta.files
}

# Function: Build package via Docker (Ubuntu/Cloud)
build_docker() {
    echo ":: Building via Docker (Arch Container)..."
    sudo rm -rf "$REPO_DIR" && mkdir -p "$REPO_DIR"
    
    docker run --privileged --rm \
        -v "$(pwd):/repo" \
        -v "$REPO_DIR:/out" \
        "$CONTAINER_IMAGE" \
        bash -c "
            pacman-key --init && pacman-key --populate archlinux && \
            pacman -Syu --noconfirm base-devel git && \
            useradd -m build && chown -R build:build /repo && \
            cd /repo && \
            for pkg in */; do \
                if [ -d \"\$pkg\" ] && [ -f \"\$pkg/PKGBUILD\" ]; then \
                    echo ':: Processing \$pkg' && \
                    (cd \"\$pkg\" && su build -c 'makepkg -scfd --noconfirm') \
                fi \
            done && \
            find . -name '*.pkg.tar.zst' -exec cp -f {} /out/ \; && \
            cd /out && \
            repo-add archcosta.db.tar.gz *.pkg.tar.zst && \
            ln -sf archcosta.db.tar.gz archcosta.db && \
            ln -sf archcosta.files.tar.gz archcosta.files
        "
}

# Execution Logic
if command -v pacman >/dev/null 2>&1 && [ -f /etc/arch-release ]; then
    build_native
else
    if command -v docker >/dev/null 2>&1; then
        build_docker
    else
        echo "❌ Error: This script requires either Arch Linux or Docker installed."
        exit 1
    fi
fi

echo "--------------------------------------------------"
echo "✅ Repo Build Finished!"
echo "Database Location: $REPO_DIR"
echo "--------------------------------------------------"
