function update_system() {
    apt-get update
    
    apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common -y
    
    apt-get install build-essential \
    git m4 unzip rsync curl bubblewrap \
    libev-dev libgmp-dev pkg-config \
    libhidapi-dev jbuilder -y
    apt-get install libsm6 libxrender1 libfontconfig1 -y
}

function install_python3() {
    sudo apt-get install virtualenv -y
    sudo apt-get install python3.6-dev -y
    sudo apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip -y
}

function setup_app() {
    git clone https://github.com/ankitchiplunkar/myhealthcheck.git
    cd myhealthcheck
    virtualenv -p python3.6 venv
    source venv/bin/activate
    pip install -r requirements.txt
}