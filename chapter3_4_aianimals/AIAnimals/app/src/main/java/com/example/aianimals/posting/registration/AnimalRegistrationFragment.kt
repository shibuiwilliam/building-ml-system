package com.example.aianimals.posting.registration

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.*
import android.widget.*
import androidx.activity.OnBackPressedCallback
import androidx.fragment.app.Fragment
import com.bumptech.glide.Glide
import com.example.aianimals.R
import com.example.aianimals.listing.detail.AnimalDetailActivity
import com.example.aianimals.listing.listing.AnimalListActivity
import com.example.aianimals.posting.camera.CameraActivity

class AnimalRegistrationFragment : Fragment(), AnimalRegistrationContract.View {
    private val TAG = AnimalRegistrationFragment::class.java.simpleName

    override lateinit var presenter: AnimalRegistrationContract.Presenter

    private lateinit var registrationImageView: ImageView
    private lateinit var takePhotoButton: Button
    private lateinit var animalNameEdit: TextView
    private lateinit var animalDescriptionEdit: TextView
    private lateinit var registerButton: Button
    private lateinit var popupBackgroundLayout: FrameLayout

    private lateinit var registrationPopupView: View
    private lateinit var registrationPopup: PopupWindow
    private lateinit var popupConfirmationButton: Button
    private lateinit var popupCancellationButton: Button

    override fun showImage(imageUri: String?) {
        if (imageUri == null) {
            registrationImageView.setImageResource(R.mipmap.ic_launcher)
        } else {
            Glide.with(this).load(imageUri).into(registrationImageView)
        }

        registrationImageView.visibility = View.VISIBLE
    }

    override fun registerAnimal() {
        saveCurrentValues()

        val animal = presenter.makeAnimal()
        if (animal == null) {
            Toast.makeText(
                context,
                "name, description and image are required",
                Toast.LENGTH_SHORT)
                .show()
        } else {
            presenter.addAnimal(animal)
            presenter.clearCurrentValues()
            val intent = Intent(context, AnimalDetailActivity::class.java).apply {
                putExtra(AnimalDetailActivity.EXTRA_ANIMAL_ID, animal.id)
            }
            startActivity(intent)
        }
    }

    override fun setAnimalName(animalName: String) {
        this.animalNameEdit.text = animalName
    }

    override fun setAnimalDescription(animalDescription: String) {
        this.animalDescriptionEdit.text = animalDescription
    }

    override fun saveCurrentValues() {
        presenter.setAnimalName(animalNameEdit.text.toString())
        presenter.setAnimalDescription(animalDescriptionEdit.text.toString())
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
            R.layout.animal_registration_fragment,
            container,
            false
        )

        with(root) {
            activity?.title = getString(R.string.animal_registration)

            registrationImageView = findViewById(R.id.registration_image)
            takePhotoButton = findViewById(R.id.take_photo_button)
            animalNameEdit = findViewById(R.id.animal_name_edit)
            animalDescriptionEdit = findViewById(R.id.animal_description_edit)
            registerButton = findViewById(R.id.register_button)

            popupBackgroundLayout = findViewById(R.id.popup_background)
            registrationPopupView = LayoutInflater.from(requireContext())
                .inflate(
                    R.layout.animal_registration_popup,
                    container,
                    false)
            registrationPopup = PopupWindow(registrationPopupView)
            registrationPopup.height = registrationPopupView.layoutParams.height
            registrationPopup.width = registrationPopupView.layoutParams.width
            popupConfirmationButton = registrationPopupView.findViewById(R.id.confirmation_button)
            popupCancellationButton = registrationPopupView.findViewById(R.id.cancellation_button)

            takePhotoButton.apply {
                setOnClickListener {
                    saveCurrentValues()
                    val intent = Intent(context, CameraActivity::class.java)
                    startActivity(intent)
                }
            }

            registrationPopup.apply {
                isOutsideTouchable = true
                isFocusable = true

                setOnDismissListener {
                    popupBackgroundLayout.visibility = View.GONE
                }
            }

            registerButton.apply {
                setOnClickListener {
                    popupBackgroundLayout.visibility = View.VISIBLE
                    registrationPopup.showAtLocation(
                        root,
                        Gravity.CENTER,
                        0,
                        0)
                }
            }

            popupBackgroundLayout.apply {
                setOnClickListener {
                    popupBackgroundLayout.visibility = View.GONE
                    registrationPopup.dismiss()
                }
            }

            popupConfirmationButton.apply {
                setOnClickListener {
                    registerAnimal()
                    popupBackgroundLayout.visibility = View.GONE
                    registrationPopup.dismiss()
                }
            }

            popupCancellationButton.apply {
                setOnClickListener {
                    popupBackgroundLayout.visibility = View.GONE
                    registrationPopup.dismiss()
                }
            }

            requireActivity().onBackPressedDispatcher.addCallback(
                this@AnimalRegistrationFragment,
                object : OnBackPressedCallback(true) {
                    override fun handleOnBackPressed() {
                        saveCurrentValues()
                        val intent = Intent(context, AnimalListActivity::class.java)
                        startActivity(intent)
                    }
                })
        }

        return root
    }

    companion object {
        private val ARGUMENT_IMAGE_URI: String? = null

        fun newInstance(imageUri: String?) = AnimalRegistrationFragment().apply {
            arguments = Bundle().apply {
                putString(ARGUMENT_IMAGE_URI, imageUri)
            }
        }
    }
}