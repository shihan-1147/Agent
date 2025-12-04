# 启动脚本 - 小米 YU7 智能助手

Write-Host "🚗 启动小米 YU7 智能助手..." -ForegroundColor Green
Write-Host ""

# 检查是否在正确的目录
if (-not (Test-Path "app.py")) {
    Write-Host "❌ 错误：请在 my_agent 目录下运行此脚本！" -ForegroundColor Red
    exit 1
}

# 检查 .env 文件
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  警告：未找到 .env 文件，请先配置 API 密钥！" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# 检查数据文件
if (-not (Test-Path "data\xiaomiYU7.docx")) {
    Write-Host "⚠️  警告：未找到数据文件 data\xiaomiYU7.docx" -ForegroundColor Yellow
    Write-Host "请先将文档文件放到 data 目录下" -ForegroundColor Yellow
    Write-Host ""
    
    # 询问是否复制文件
    $source = "E:\Agent\AI助手\xiaomiYU7.docx"
    if (Test-Path $source) {
        $copy = Read-Host "是否从旧目录复制文件？(Y/N)"
        if ($copy -eq "Y" -or $copy -eq "y") {
            Copy-Item $source -Destination "data\xiaomiYU7.docx" -Force
            Write-Host "✅ 文件复制成功！" -ForegroundColor Green
        } else {
            exit 1
        }
    } else {
        exit 1
    }
}

Write-Host "✅ 环境检查通过！" -ForegroundColor Green
Write-Host ""
Write-Host "📖 使用说明：" -ForegroundColor Cyan
Write-Host "  - 在浏览器中会自动打开应用界面" -ForegroundColor Gray
Write-Host "  - 按 Ctrl+C 可停止服务" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 正在启动 Streamlit..." -ForegroundColor Green
Write-Host ""

# 激活虚拟环境（如果存在）
$pythonPath = "E:\AI_Envs\ai_agent\python.exe"
if (Test-Path $pythonPath) {
    Write-Host "使用 Python: $pythonPath" -ForegroundColor Cyan
    & $pythonPath -m streamlit run app.py
} else {
    Write-Host "使用系统 Python" -ForegroundColor Cyan
    streamlit run app.py
}
