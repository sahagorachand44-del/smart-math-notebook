name: Build Android APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install system dependencies
      run: |
        sudo apt update
        sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
          autoconf automake libtool pkg-config zlib1g-dev \
          libncurses5-dev libncursesw5-dev libtinfo5 cmake \
          libffi-dev libssl-dev build-essential gettext libltdl-dev

    - name: Install Python dependencies
      run: |
        pip install --upgrade pip "setuptools<70" wheel
        pip install "Cython==0.29.36" "buildozer==1.5.0" virtualenv

    - name: Cache Buildozer
      uses: actions/cache@v4
      with:
        path: |
          ~/.buildozer
          .buildozer
        key: buildozer-${{ hashFiles('buildozer.spec') }}

    - name: Build with Buildozer
      run: |
        set +o pipefail
        yes | buildozer -v android debug > build_full.log 2>&1

    - name: Show real error
      if: failure()
      run: |
        echo "=== LAST 80 LINES ==="
        tail -n 80 build_full.log
        echo "=== ERROR LINES ==="
        grep -n -E "error:|Error [0-9]|\\\*|Command failed|FAILED|fatal" build_full.log | tail -n 30

    - name: Upload full log
      if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: build-log
        path: build_full.log

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: smart-math-apk
        path: bin/*.apk
