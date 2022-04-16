package com.example.aianimals.service

import android.content.Context
import android.content.res.AssetManager
import java.io.FileInputStream
import java.io.IOException
import java.nio.MappedByteBuffer
import java.nio.channels.FileChannel
import java.nio.channels.FileChannel.MapMode


class ModelLoader(context: Context) {
    private var assetManager: AssetManager = context.assets

    @Throws(IOException::class)
    fun loadMappedFile(directoryName: String, filePath: String): MappedByteBuffer? {
        val fileDescriptor = assetManager.openFd("$directoryName/$filePath")
        val inputStream = FileInputStream(fileDescriptor.fileDescriptor)
        val fileChannel: FileChannel = inputStream.channel
        val startOffset = fileDescriptor.startOffset
        val declaredLength = fileDescriptor.declaredLength
        return fileChannel.map(MapMode.READ_ONLY, startOffset, declaredLength)
    }
}