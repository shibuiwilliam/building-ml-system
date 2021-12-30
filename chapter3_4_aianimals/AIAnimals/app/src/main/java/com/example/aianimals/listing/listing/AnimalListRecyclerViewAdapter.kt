package com.example.aianimals.listing.listing

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.aianimals.R
import com.example.aianimals.repository.animal.Animal
import com.google.android.material.floatingactionbutton.ExtendedFloatingActionButton
import com.google.android.material.floatingactionbutton.FloatingActionButton

class AnimalListRecyclerViewAdapter(
    context: Context,
    animals: Map<String, Animal>
) : RecyclerView.Adapter<AnimalListRecyclerViewAdapter.AnimalListRecyclerViewHolder>() {
    private val TAG = AnimalListRecyclerViewAdapter::class.java.simpleName

    var animals: List<Animal> = animals.values.toList()
        set(animals) {
            field = animals
            notifyDataSetChanged()
        }

    private var context: Context = context

    private lateinit var onAnimalCellClickListener: OnAnimalCellClickListener

    interface OnAnimalCellClickListener {
        fun onItemClick(animal: Animal)
    }

    fun setOnAnimalCellClickListener(onAnimalCellClickListener: OnAnimalCellClickListener) {
        this.onAnimalCellClickListener = onAnimalCellClickListener
    }

    override fun onCreateViewHolder(
        parent: ViewGroup,
        viewType: Int
    ): AnimalListRecyclerViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        val view = inflater.inflate(R.layout.animal_list_fragment_cell, parent, false)
        return AnimalListRecyclerViewHolder(view)
    }

    override fun onBindViewHolder(holder: AnimalListRecyclerViewHolder, position: Int) {
        val animal = animals[position]
        Glide.with(context).load(animal.imageUrl).into(holder.animalImageView)
        holder.animalLikesButton.text = animal.likes.toString()
        holder.itemView.setOnClickListener {
            onAnimalCellClickListener.onItemClick(animal)
        }
    }

    override fun getItemCount(): Int {
        return animals.size
    }

    inner class AnimalListRecyclerViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        var animalImageView: ImageView = itemView.findViewById(R.id.animal_image)
        var animalLikesButton: ExtendedFloatingActionButton = itemView.findViewById(R.id.animal_likes)
    }
}