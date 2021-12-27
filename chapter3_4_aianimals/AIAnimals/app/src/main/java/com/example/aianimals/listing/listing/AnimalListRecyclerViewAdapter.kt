package com.example.aianimals.listing.listing

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.recyclerview.widget.RecyclerView
import com.example.aianimals.R
import com.example.aianimals.repository.Animal

class AnimalListRecyclerViewAdapter(
    animals: Map<Int, Animal>
) : RecyclerView.Adapter<AnimalListRecyclerViewAdapter.AnimalListRecyclerViewHolder>() {
    var animals: Map<Int, Animal> = animals
        set(animals) {
            field = animals
            notifyDataSetChanged()
        }

    private lateinit var onAnimalCellClickListener: OnAnimalCellClickListener

    interface OnAnimalCellClickListener {
        fun onItemClick(animal: Animal)
    }

    fun setOnAnimalCellClickListener(onAnimalCellClickListener: OnAnimalCellClickListener) {
        this.onAnimalCellClickListener = onAnimalCellClickListener
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): AnimalListRecyclerViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        val view = inflater.inflate(R.layout.animal_list_fragment_cell, parent, false)
        return AnimalListRecyclerViewHolder(view)
    }

    override fun onBindViewHolder(holder: AnimalListRecyclerViewHolder, position: Int) {
        val animal = animals[position]!!
        holder.animalName.text = animal.name
        holder.animalPrice.text = animal.price.toString()
        holder.animalPurchaseDate.text = animal.date
        holder.itemView.setOnClickListener{
            onAnimalCellClickListener.onItemClick(animal)
        }
    }

    override fun getItemCount(): Int {
        return animals.size
    }

    inner class AnimalListRecyclerViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        var animalName: TextView
        var animalPrice: TextView
        var animalPurchaseDate: TextView

        init {
            animalName = itemView.findViewById(R.id.tv_animal_name)
            animalPrice = itemView.findViewById(R.id.tv_animal_price)
            animalPurchaseDate = itemView.findViewById(R.id.tv_animal_purchase_date)
        }
    }
}