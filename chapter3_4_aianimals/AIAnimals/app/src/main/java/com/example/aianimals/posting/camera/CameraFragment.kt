package com.example.aianimals.posting.camera

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.example.aianimals.R

class CameraFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root =  inflater.inflate(
            R.layout.camera_fragment,
            container,
            false)

        with (root) {

        }

        return root
    }

    companion object {
        fun newInstance() = CameraFragment()
    }
}