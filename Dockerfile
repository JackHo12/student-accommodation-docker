FROM python:3.11-slim

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates fonts-liberation \
    libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libdrm2 libgbm1 \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Chrome for Testing v135
ENV CHROME_VERSION=135.0.7049.95

RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip" -O /tmp/chrome.zip && \
    unzip /tmp/chrome.zip -d /opt && \
    ln -s /opt/chrome-linux64/chrome /usr/bin/google-chrome && \
    rm /tmp/chrome.zip

# 安裝對應版本的 ChromeDriver
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /tmp && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver*

# 安裝 Python 相依
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY get_student_accommodation.py .

# 啟動程式
CMD ["python", "get_student_accommodation.py"]
