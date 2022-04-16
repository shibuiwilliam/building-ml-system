package com.example.aianimals.service

import org.tensorflow.lite.Interpreter
import java.lang.Exception
import java.nio.ByteBuffer
import java.nio.FloatBuffer
import java.nio.MappedByteBuffer

class PersonalizedModel(private var modelLoader: ModelLoader) {
    private lateinit var model: MappedByteBuffer
    private var interpreter: Interpreter

    init {
        loadModel()
        this.interpreter = Interpreter(this.model)
    }

    private fun loadModel() {
        val loadedModel = this.modelLoader.loadMappedFile(MODEL_NAME) ?: throw Exception("")
        this.model = loadedModel
    }

    fun runTraining(features: Array<FloatArray>, labels: Array<FloatArray>): Float {
        val inputs: MutableMap<String, Any> = mutableMapOf()
        inputs["x"] = features
        inputs["y"] = labels
        val outputs: MutableMap<String, Any> = mutableMapOf()
        val loss: FloatBuffer = FloatBuffer.allocate(1)
        outputs["loss"] = loss
        interpreter.runSignature(inputs, outputs, "train")
        return loss.get(0)
    }

    fun runInference(testImage: Array<Array<FloatArray>>): FloatArray? {
        val inputs: MutableMap<String, Any> = HashMap()
        inputs["x"] = arrayOf(testImage)
        val outputs: MutableMap<String, Any> = HashMap()
        val output = Array(1) { FloatArray(NUM_CLASSES) }
        outputs["output"] = output
        interpreter.runSignature(inputs, outputs, "infer")
        return output[0]
    }

    fun close() {
        this.interpreter.close()
    }

    companion object{
        const val MODEL_NAME = "model_personalization.tflite"
        const val INPUT_SIZE = 1024
        const val BATCH_SIZE = 16
        const val NUM_CLASSES = 2
    }
}