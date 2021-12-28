package com.example.aianimals.posting.camera

import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView

interface CameraContract {
    interface Presenter: BasePresenter{
        fun takePhoto()
        fun saveImageFile()
    }

    interface View: BaseView<Presenter>{
        fun takePhoto()
    }
}