# Index - Android App

简易海外网站导航的 Android APK 封装。

## 项目结构

```
android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── assets/web/          # 网站静态资源（本地加载）
│   │   │   │   ├── index.html
│   │   │   │   ├── manifest.json
│   │   │   │   ├── sw.js
│   │   │   │   ├── css/
│   │   │   │   └── proxys/
│   │   │   ├── java/.../MainActivity.java  # 主Activity
│   │   │   ├── res/                        # 资源文件
│   │   │   └── AndroidManifest.xml
│   │   └── build.gradle
│   └── proguard-rules.pro
├── gradle/wrapper/
├── gradlew.bat
├── gradlew (Unix)
├── build.gradle
├── settings.gradle
├── gradle.properties
└── generate_icons.py         # 图标生成脚本
```

## 构建方式

### 方式一：Android Studio（推荐）

1. 打开 Android Studio → `File → Open...`
2. 选择 `html/simple_index/android` 目录
3. 等待 Gradle 同步完成
4. `Build → Build Bundle(s) / APK(s) → Build APK(s)`
5. 生成的 APK 在 `app/build/outputs/apk/debug/`

### 方式二：命令行

```bash
# 先确认安装了 JDK 并设置了 JAVA_HOME
cd html/simple_index/android
./gradlew assembleDebug
```

### 方式三：使用 Gradle Wrapper

```bash
cd html/simple_index/android
gradlew.bat assembleDebug
```

## 功能特性

- ✅ 本地加载网站（无需网络即可打开）
- ✅ 站外链接自动用系统浏览器打开
- ✅ PWA 支持（manifest + Service Worker）
- ✅ 液态玻璃切换
- ✅ 暗色模式自适应（Android 10+）
- ✅ 进度条显示加载状态
- ✅ 沉浸式状态栏
- ✅ 手机和平板双端适配

## 技术要求

- **Android SDK**: compileSdk 34 / targetSdk 34 / minSdk 21
- **Java**: JDK 17+
- **Android Studio**: Arctic Fox (2020.3.1) 或更高版本

## 更换图标

如果需要更换图标，替换 `app/src/main/res/ic_source.jpg`，然后运行：

```bash
python generate_icons.py