package com.example.aianimals.posting.camera

import com.example.aianimals.repository.animal.source.AnimalRepository
import java.io.File

class CameraPresenter(
    private val outputDirectory: File,
    private val animalRepository: AnimalRepository,
    private val cameraView: CameraContract.View
) : CameraContract.Presenter {
    init {
        this.cameraView.presenter = this
    }

    override fun start() {
        cameraView.checkPermission()
    }

    override fun takePhoto() {
        cameraView.takePhoto(outputDirectory)
    }

    override fun saveImageFile() {
    }
}