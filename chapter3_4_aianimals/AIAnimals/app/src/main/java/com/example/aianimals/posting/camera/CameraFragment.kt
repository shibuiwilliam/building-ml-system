package com.example.aianimals.posting.camera

import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.Toast
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageCaptureException
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import com.example.aianimals.R
import com.example.aianimals.middleware.Permission
import com.example.aianimals.posting.registration.AnimalRegistrationActivity
import java.io.File
import java.text.SimpleDateFormat

class CameraFragment : Fragment(), CameraContract.View {
    private val TAG = CameraFragment::class.java.simpleName

    override lateinit var presenter: CameraContract.Presenter

    private lateinit var previewFinder: PreviewView
    private lateinit var camera_capture_button: Button
    private var imageCapture: ImageCapture? = null

    override fun checkPermission() {
        if (Permission.allPermissionsGranted(requireContext())) {
            startCamera()
        } else {
            requestPermissions(
                Permission.REQUIRED_PERMISSIONS,
                Permission.REQUEST_CODE_PERMISSIONS
            )
        }
    }

    override fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(requireContext())

        cameraProviderFuture.addListener(
            Runnable
            {
                val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()

                val preview = Preview
                    .Builder()
                    .build()
                    .also {
                        it.setSurfaceProvider(previewFinder.surfaceProvider)
                    }

                this.imageCapture = ImageCapture
                    .Builder()
                    .build()

                val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

                try {
                    cameraProvider.unbindAll()
                    cameraProvider.bindToLifecycle(
                        this,
                        cameraSelector,
                        preview,
                        this.imageCapture
                    )

                } catch (e: Exception) {
                    Log.e(TAG, "Use case binding failed", e)
                }

            }, ContextCompat.getMainExecutor(requireContext())
        )
    }

    override fun takePhoto(outputDirectory: File) {
        val imageCapture = this.imageCapture ?: return

        val photoFile = File(
            outputDirectory,
            SimpleDateFormat("yyyy-MM-dd-HH-mm-ss-SSS")
                .format(System.currentTimeMillis()) + ".jpg"
        )

        Log.i(TAG, "taking photo ${photoFile}")
        val outputOptions = ImageCapture
            .OutputFileOptions
            .Builder(photoFile)
            .build()

        imageCapture.takePicture(
            outputOptions,
            ContextCompat.getMainExecutor(requireContext()),
            object : ImageCapture.OnImageSavedCallback {
                override fun onError(exc: ImageCaptureException) {
                    Log.e(TAG, "Photo capture failed: ${exc.message}", exc)
                }

                override fun onImageSaved(output: ImageCapture.OutputFileResults) {
                    val savedUri = Uri.fromFile(photoFile)
                    val msg = "Photo capture succeeded: ${savedUri}"
                    Toast.makeText(context, msg, Toast.LENGTH_SHORT).show()
                    Log.i(TAG, msg)

                    val intent = Intent(context, AnimalRegistrationActivity::class.java).apply {
                        putExtra(AnimalRegistrationActivity.IMAGE_URI, savedUri.toString())
                    }
                    startActivity(intent)
                }
            })
    }

    override fun onResume() {
        super.onResume()
        presenter.start()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root = inflater.inflate(
            R.layout.camera_fragment,
            container,
            false
        )

        with(root) {
            activity?.title = getString(R.string.camera)

            previewFinder = findViewById(R.id.preview_finder)
            camera_capture_button = findViewById(R.id.camera_capture_button)

            camera_capture_button.apply {
                setOnClickListener {
                    presenter.takePhoto()
                }
            }

        }
        return root
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == Permission.REQUEST_CODE_PERMISSIONS) {
            if (PackageManager.PERMISSION_GRANTED == grantResults.firstOrNull()) {
                // Take the user to the success fragment when permission is granted
                Toast.makeText(context, "Permission request granted", Toast.LENGTH_LONG).show()
                startCamera()
            } else {
                Toast.makeText(context, "Permission request denied", Toast.LENGTH_LONG).show()
            }
        }
    }

    companion object {
        fun newInstance() = CameraFragment()
    }
}