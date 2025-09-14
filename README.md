# 🚀 MarketPulse Dashboard

A comprehensive marketing intelligence and business performance analytics dashboard built with Streamlit. MarketPulse provides actionable insights from multi-channel marketing data to optimize campaign performance and drive business growth.

![MarketPulse Logo](assets/Logo.svg)

## 📊 Features

- **Multi-Channel Analytics**: Analyze performance across Facebook, Google, and TikTok campaigns
- **Business Impact Analysis**: Track revenue attribution and marketing ROI
- **Real-time Performance Alerts**: Get notified of significant performance changes
- **Interactive Visualizations**: Dynamic charts and graphs powered by Plotly
- **Channel Comparison**: Compare performance metrics across different marketing channels
- **Business Intelligence**: Strategic insights and actionable recommendations
- **Responsive Design**: Clean, modern UI with intuitive navigation

## 🏗️ Project Structure

```
MarketPulse/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── assets/
│   ├── Logo.svg          # Application logo
│   └── style.css         # Custom styling
├── components/
│   ├── __init__.py
│   ├── charts.py         # Chart components
│   ├── metrics.py        # Metric calculations
│   └── utils.py          # Utility functions
├── data/
│   ├── Facebook.csv      # Facebook campaign data
│   ├── Google.csv        # Google Ads data
│   ├── TikTok.csv        # TikTok campaign data
│   └── Business.csv      # Business revenue data
├── pages/
│   ├── 1_Overview.py     # Executive overview page
│   ├── 2_Channel_Analysis.py  # Channel deep dive
│   ├── 3_Business_Impact.py   # Business metrics
│   └── 4_Business_Intelligence.py  # Strategic insights
└── src/
    ├── analytics.py      # Core analytics engine
    └── data_processor.py # Data processing utilities
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd MarketPulse
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv marketpulse_env

# Activate virtual environment
# On Windows:
marketpulse_env\Scripts\activate

# On macOS/Linux:
source marketpulse_env/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Prepare Data Files

Ensure your CSV files are placed in the `data/` directory:

- `Facebook.csv` - Facebook campaign data
- `Google.csv` - Google Ads data  
- `TikTok.csv` - TikTok campaign data
- `Business.csv` - Business revenue data

**Required CSV Columns:**

**Facebook.csv / Google.csv / TikTok.csv:**
- `Date` - Campaign date (YYYY-MM-DD format)
- `Spend` - Marketing spend amount
- `Impressions` - Number of impressions
- `Clicks` - Number of clicks
- `Channel` - Marketing channel name

**Business.csv:**
- `Date` - Business date (YYYY-MM-DD format)
- `Revenue` - Daily revenue amount

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🚀 Usage

1. **Home Dashboard**: Overview of key performance indicators and marketing metrics
2. **Overview**: Executive summary with high-level insights
3. **Channel Analysis**: Deep dive into individual channel performance
4. **Business Impact**: Revenue attribution and ROI analysis
5. **Business Intelligence**: Strategic recommendations and insights

## 📋 Requirements

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
numpy>=1.24.0
python-dateutil>=2.8.0
```

## 🔧 Configuration

### Streamlit Configuration

The `.streamlit/config.toml` file contains application settings:

```toml
[theme]
primaryColor = "#3366FF"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
headless = true
port = 8501
```

### Environment Variables

No environment variables are required for basic functionality.

## 🌐 Deployment

### Option 1: Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Option 2: Heroku

1. Create a `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

### Option 3: Docker

1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

2. Build and run:
```bash
docker build -t marketpulse .
docker run -p 8501:8501 marketpulse
```

## 🐛 Troubleshooting

### Common Issues

1. **Module not found errors**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

2. **Data loading errors**: Verify CSV files are in the correct format and location

3. **Port already in use**: Change the port in the run command
```bash
streamlit run app.py --server.port 8502
```

4. **Memory issues**: For large datasets, consider data sampling or optimization

### Performance Optimization

- Use data caching with `@st.cache_data`
- Optimize CSV file sizes
- Consider using Parquet format for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Email: support@marketpulse.com

## 🔄 Version History

- **v1.0.0** - Initial release with core analytics features
- **v1.1.0** - Added business intelligence module
- **v1.2.0** - Enhanced UI/UX and performance improvements

---

**Built with ❤️ using Streamlit**