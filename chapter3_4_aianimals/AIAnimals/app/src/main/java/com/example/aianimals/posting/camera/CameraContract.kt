package com.example.aianimals.posting.camera

import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView
import java.io.File

interface CameraContract {
    interface Presenter : BasePresenter {
        fun takePhoto()
        fun saveImageFile()
    }

    interface View : BaseView<Presenter> {
        fun checkPermission()
        fun startCamera()
        fun takePhoto(outputDirectory: File)
    }
}