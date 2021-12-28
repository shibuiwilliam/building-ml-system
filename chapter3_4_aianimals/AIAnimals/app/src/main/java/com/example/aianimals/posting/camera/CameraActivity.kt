package com.example.aianimals.posting.camera

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.example.aianimals.Injection
import com.example.aianimals.R
import com.example.aianimals.middleware.Permission
import java.io.File
import java.util.concurrent.ExecutorService

class CameraActivity : AppCompatActivity() {
    private lateinit var cameraPresenter: CameraPresenter

    private lateinit var cameraExecutor: ExecutorService

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.camera_activity)

        val cameraFragment = supportFragmentManager
            .findFragmentById(R.id.camera_activity_frame)
                as CameraFragment? ?: CameraFragment.newInstance().also {
            supportFragmentManager
                .beginTransaction()
                .replace(R.id.camera_activity_frame, it)
                .commit()
        }

        cameraPresenter = CameraPresenter(
            getOutputDirectory(),
            Injection.provideAnimalRepository(applicationContext),
            cameraFragment
        )
    }

    override fun onDestroy() {
        super.onDestroy()
        cameraExecutor.shutdown()
    }

    private fun getOutputDirectory(): File {
        val mediaDir = externalMediaDirs
            .firstOrNull()?.let {
            File(it, resources.getString(R.string.app_name))
                .apply {
                    mkdirs()
                }
            }
        return if (mediaDir != null && mediaDir.exists())
            mediaDir else filesDir
    }
}