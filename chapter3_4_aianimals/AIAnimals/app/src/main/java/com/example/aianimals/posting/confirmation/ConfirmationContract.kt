package com.example.aianimals.posting.confirmation

import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView
import com.example.aianimals.repository.animal.Animal

interface ConfirmationContract {
    interface Presenter : BasePresenter {
        fun showAnimal()
        fun confirmRegistration()
        fun cancelRegistration()
    }

    interface View : BaseView<Presenter> {
        fun showAnimal(animal: Animal)
        fun confirmRegistration(animal: Animal)
        fun cancelRegistration()
    }
}