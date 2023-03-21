# 📺 YouTube Trend Visualizer

![Demo](img/dash_dashboard.gif)

Contributors: Lauren Zung

Live Server: https://youtube-trend-visualizer.onrender.com/

## Proposal

Click [here](https://github.com/UBC-MDS/trending_youtube_viz_R/blob/main/reports/proposal.md) to read the initial motivation and purpose of this dashboard.

## Dashboard Features

This dashboard features a single landing page that allows users to easily visualize YouTube video metrics. There is a calendar widget that can be configured to focus on trending videos between a date range. If desired, users can apply an additional filter using the dropdown category menu, which can be parsed by selecting and/or searching for topics of interest. These filters will update the settings for each plot and table, allowing for improved visibility and interpretation of trends over time. Aggregate counts of the number of videos and channels are also displayed to provide a comprehensive overview on the amount of data points displayed.

### 😀 Polarity Score Chart 😩

### 📈 Category Trend Chart 📉


## Usage

To run this dashboard locally and/or use your own data collected from the YouTube API, clone this repository and download the environment found [here](https://github.com/lzung/youtube_trends/blob/main/environment.yaml) to install the necessary [dependencies](#dependencies).

1. Clone the repository

```bash
git clone https://github.com/lzung/youtube_trends.git
```

2. Navigate to the repository

```bash
cd youtube_trends
```

3. Create the environment

```bash
conda env create -f environment.yaml
```

Assuming that the environment was created successfully, you can activate the environment as follows:

```bash
conda activate youtube_trends
```

4. Navigate to the `src` folder and run `app.py` to render the dashboard locally. If you want to add your own dataset, first import your data (as a `.csv`), then run the `feature_engineering.py` script to export before deploying the dashboard.

```bash
cd src
python3 app.py
```

## Dependencies
The associated environment with all dependencies required for this project can be found [here](https://github.com/lzung/youtube_trends/blob/main/environment.yaml).
- python==3.11.*
- ipykernel
- vega_datasets
- altair
- dash=2.8.*
- dash-bootstrap-components
- nltk
- pip:
    - dash-iconify
    - dash-mantine-components

## Live Dashboard

The dashboard is deployed on Render. You can view and interact with the app by [clicking here](https://youtube-trend-visualizer.onrender.com/).

## References

Youtube. (2023). YouTube Trending Video Dataset (updated daily) [Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/5003820

Note: As I'm based in Canada, I am using data extracted from videos that were trending in Canada due to file size limitations and for ease of loading/extraction. However, given the flexibility of this web app, it can be easily extended to YouTube data from other countries.
