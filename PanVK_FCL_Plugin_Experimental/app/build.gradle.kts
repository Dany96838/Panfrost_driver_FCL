plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.jetbrains.kotlin.android)
}

android {
    namespace = "com.mio.plugin.renderer"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.mio.plugin.renderer.panvk2631"
        minSdk = 35
        targetSdk = 35
        versionCode = 1
        versionName = "26.3.1-experimental"
    }

    buildTypes {
        release { isMinifyEnabled = false }
        configureEach {
            resValue("string", "app_name", "Mesa PanVK 26.3.1 experimental")
            manifestPlaceholders["driver"] = "Mesa PanVK 26.3.1 experimental (Mali)"
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    kotlinOptions { jvmTarget = "1.8" }
}

dependencies {}
