package com.example.aianimals.listing

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.setFragmentResultListener
import com.example.aianimals.R
import kotlinx.android.synthetic.main.fragment_animal.*

class AnimalFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_animal, container, false)
        activity?.title = getString(R.string.item_detail)
        setFragmentResultListener("animalData") {_, bundle ->
            tv_animal_name.text = bundle.getString("animalName")
            tv_animal_price.text = bundle.getInt("animalPrice").toString()
            tv_animal_purchase_date.text = bundle.getString("animalPurchaseDate")
        }
        return view
    }
}