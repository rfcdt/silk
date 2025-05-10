# Unified Asset Aggregator

This project fetches and merges host asset data from multiple sources (e.g., Qualys, CrowdStrike), normalizes them, and stores the results in MongoDB.

## 🧰 Prerequisites

- Python 3.10+
- Docker & Docker Compose
- `make` installed

## 🚀 Getting Started

### 1. Clone the repository

```
git clone git@github.com:rfcdt/silk.git
cd silk
```

### 2. Set Up Environment Variables

Copy the example .env to .env.local:
```
cp .env .env.local
```
Then edit .env.local to include your API key
```
API_KEY=<API_KEY>
```
### 3. Create Virtual Environment & Install Dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Start MongoDB
You can start MongoDB using either Docker Compose or Makefile:
```
docker compose up -d
# or
make up
```

### 5. Run the Application
Use the --source argument to choose the data source:
```
python main.py --source qualys
python main.py --source crowdstrike
```

## Examples
Count grouped by OS and hostname
![Count grouped by OS and hostname](https://github.com/rfcdt/silk/blob/master/examples/group_by_os_host.png?raw=true)

Count grouped by OS
![Count grouped by OS](https://github.com/rfcdt/silk/blob/master/examples/group_by_os.png?raw=true)

Here you can see merged fields what they have nested objects like qualys and crowdstrike. I did it because such fields have different values in APIs and to merge them I created those nested objects.
If you take a look at the account object, it doesn't have nested objects like before, because values of it are in qualys API only. And in theory, there is no issue to add more usernames from others API.
![One of merged host](https://github.com/rfcdt/silk/blob/master/examples/one_of_merged_host.png?raw=true)