package com.example.aianimals.service

import android.graphics.Bitmap
import android.util.Log
import org.tensorflow.lite.DataType
import org.tensorflow.lite.Interpreter
import org.tensorflow.lite.gpu.GpuDelegate
import org.tensorflow.lite.support.common.ops.NormalizeOp
import org.tensorflow.lite.support.image.ImageProcessor
import org.tensorflow.lite.support.image.TensorImage
import org.tensorflow.lite.support.image.ops.ResizeOp
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer
import java.nio.MappedByteBuffer

class FeatureExtractionModel(private var modelLoader: ModelLoader) {
    private val TAG = FeatureExtractionModel::class.java.simpleName

    private lateinit var model: MappedByteBuffer
    private lateinit var interpreter: Interpreter
    private lateinit var imageProcessor: ImageProcessor

    init {
        loadModel()
        initInterpreter()
        initImageProcessor()
    }

    private fun loadModel() {
        val loadedModel = this.modelLoader.loadMappedFile(DIRECTORY, MODEL_NAME) ?: throw Exception("")
        this.model = loadedModel
    }

    private fun initInterpreter() {
        val options = Interpreter.Options().apply {
            when (DELEGATE) {
                DelegateOptions.CPU -> setNumThreads(NUM_THREADS)
                DelegateOptions.NNAPI -> setUseNNAPI(true)
                DelegateOptions.GPU -> addDelegate(GpuDelegate())
            }
        }
        this.interpreter = Interpreter(this.model, options)
    }

    private fun initImageProcessor() {
        this.imageProcessor = ImageProcessor
            .Builder()
            .add(ResizeOp(INPUT_HEIGHT, INPUT_WIDTH, ResizeOp.ResizeMethod.BILINEAR))
            .add(NormalizeOp(127.5f, 127.5f))
            .build()
    }

    fun preprocess(bitmap: Bitmap): TensorImage {
        val image = TensorImage(DataType.FLOAT32)
        image.load(bitmap)
        val preprocessed = this.imageProcessor.process(image)
        Log.i(TAG, "image: $preprocessed")
        return preprocessed
    }

    fun extractFeature(bitmap: Bitmap): FloatArray {
        val image = this.preprocess(bitmap)
        val feature = TensorBuffer.createFixedSize(intArrayOf(1, OUTPUT_SIZE), DataType.FLOAT32)
        interpreter.run(image.buffer, feature.buffer)
        return feature.floatArray
    }

    fun close() {
        this.interpreter.close()
    }

    sealed class DelegateOptions {
        object CPU : DelegateOptions()
        object GPU : DelegateOptions()
        object NNAPI : DelegateOptions()
    }

    companion object {
        const val DIRECTORY = "model"
        const val MODEL_NAME =
            "lite-model_imagenet_mobilenet_v3_small_100_224_feature_vector_5_default_1.tflite"
        const val INPUT_HEIGHT = 224
        const val INPUT_WIDTH = 224
        const val OUTPUT_SIZE = 1024
        const val NUM_THREADS = 4
        val DELEGATE: DelegateOptions = DelegateOptions.NNAPI

        private var INSTANCE: FeatureExtractionModel? = null

        @JvmStatic
        fun getInstance(modelLoader: ModelLoader): FeatureExtractionModel {
            return INSTANCE ?: FeatureExtractionModel(modelLoader).apply { INSTANCE = this }
        }

        @JvmStatic
        fun destroyInstance() {
            if (INSTANCE != null) {
                INSTANCE!!.close()
            }
            INSTANCE = null
        }
    }
}