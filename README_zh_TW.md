# Cursor Pro 自動化工具

[简体中文](README.md) | [繁體中文](README_zh_TW.md) | [English](README_en.md)

<p align="center">
  <img src="./assets/logo.png" alt="Cursor Pro Logo" width="200"/>
</p>

## 🚀 功能介紹
自動註冊賬號，自動刷新本地token，解放雙手。

## ⬇️ 下載地址
https://github.com/chengazhen/cursor-auto-free/releases

## ⚠️ 重要提示
1. **確保已安裝 Chrome 瀏覽器**
   - 如果未安裝，請從[官方網站下載](https://www.google.com/intl/en_pk/chrome/)

2. **必須先完成賬號登錄**
   - 不論賬號是否有效，必須先完成登錄步驟

3. **網絡要求**
   - 需要穩定的網絡連接
   - 建議使用國外節點
   - ⚠️ 切勿開啟全局代理

## 🛠️ 構建使用
### Win / Mac / Linux 通用

<p align="center">
  <img src="./screen/build_2025-01-04_11-02-45.png" alt="構建步驟 1"/>
  <img src="./screen/build_2025-01-04_11-04-43.png" alt="構建步驟 2"/>
</p>

```bash
# 根據您的操作系統選擇以下任一方式構建：
Windows: build.bat
macOS:   build.mac.command
Linux:   build.sh
```

## 📱 運行方法

### macOS
1. 打開終端，進入應用目錄
2. 授權執行權限：
```bash
chmod +x ./CursorPro
```
3. 運行程序：
```bash
./CursorPro
```
或直接在訪達（Finder）中雙擊運行

> 💡 如遇到啟動問題，請參考[解決方案](https://sysin.org/blog/macos-if-crashes-when-opening/)

<p align="center">
  <img src="./screen/c29ea438-ee74-4ba1-bbf6-25e622cdfad5.png" alt="macOS 錯誤示例"/>
</p>

### Windows
直接雙擊運行 `CursorPro.exe`

## ✅ 驗證方法
運行腳本完成後，重啟編輯器，確認賬號信息與腳本輸出日誌一致：

<p align="center">
  <img src="./screen/截屏2025-01-04 09.44.48.png" alt="驗證成功示例"/>
</p>

## 📝 使用注意事項

1. **運行環境要求**
   - 穩定的網絡連接
   - 足夠的系統權限

2. **使用過程中**
   - 請勿手動關閉瀏覽器窗口
   - 耐心等待程序自動完成操作
   - 看到"腳本執行完畢"提示後再關閉程序

## ❓ 常見問題解決

1. **程序運行卡住**
   - 檢查網絡連接
   - 重啟程序重試

## ⚖️ 免責聲明
本工具僅供學習研究使用，請遵守相關服務條款。使用本工具產生的任何後果由使用者自行承擔。

---

> 倉庫源碼來自開源；自行優化了驗證和郵箱註冊邏輯；解決了無法獲取郵箱驗證碼的問題。 