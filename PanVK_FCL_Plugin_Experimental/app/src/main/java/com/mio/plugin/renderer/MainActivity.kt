package com.mio.plugin.renderer

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(TextView(this).apply {
            text = "Mesa PanVK 26.3.1 experimental\n\nDriver Vulkan experimental para GPUs Mali.\nCompatibilidade com este dispositivo ainda não confirmada."
            textSize = 16f
            setPadding(32, 32, 32, 32)
        })
    }
}
