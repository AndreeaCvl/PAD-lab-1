package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

type Product struct {
	ProductID          string  `json:"product_id"`
	UserID             string  `json:"user_id"`
	ProductName        string  `json:"product_name"`
	ProductDescription string  `json:"product_description"`
	Price              float32 `json:"price"`
}

func CreateProduct(w http.ResponseWriter, r *http.Request) {
	var p Product

	err := json.NewDecoder(r.Body).Decode(&p)

	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	responseJSON, err := json.Marshal(p)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Send a POST request to the /add_product endpoint on localhost:5001
	resp, err := http.Post("http://localhost:5001/add_product", "application/json", bytes.NewBuffer(responseJSON))
	if err != nil {
		log.Fatal(err)
	}

	defer resp.Body.Close()

	// Log the response status code and body
	log.Printf("Response Status Code: %d", resp.StatusCode)

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("Response Body: %s", body)

	p.ProductID = string(body)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated) // HTTP status code 201 for resource creation
	json.NewEncoder(w).Encode(p)
}

func DeleteProduct(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id, ok := vars["id"]

	if !ok {
		fmt.Println("id is missing in parameters")
		http.Error(w, "Missing ID parameter", http.StatusBadRequest)
		return
	}

	url := "http://localhost:5001/products/" + id // Replace 5001 with the appropriate port number of your Python server

	req, err := http.NewRequest("DELETE", url, nil)
	if err != nil {
		fmt.Println("Error creating DELETE request:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error sending DELETE request:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	// Check the response status code
	if resp.StatusCode != http.StatusOK {
		fmt.Println("Error deleting product. Status Code:", resp.StatusCode)
		http.Error(w, "Error deleting product", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK) // HTTP status code 200 for successful deletion
	fmt.Fprintf(w, "Product with ID %s has been deleted successfully", id)
}

func SearchProductByName(w http.ResponseWriter, r *http.Request) {
	// Get the product name query parameter from the request
	productName := r.URL.Query().Get("name")

	// Send a GET request to the /products endpoint on localhost:5001
	resp, err := http.Get("http://localhost:5001/products?name=" + productName)
	if err != nil {
		fmt.Println("Error sending GET request:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	// Read the response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading response body:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Set the response headers and write the response body to the client
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(resp.StatusCode)
	w.Write(body)
}

func SearchAllProducts(w http.ResponseWriter, r *http.Request) {

	// Send a GET request to the /products endpoint on localhost:5001
	resp, err := http.Get("http://localhost:5001/products")
	if err != nil {
		fmt.Println("Error sending GET request:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	// Read the response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading response body:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Set the response headers and write the response body to the client
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(resp.StatusCode)
	w.Write(body)
}

func AddToFavorites(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	userID, ok := vars["user_id"]

	if !ok {
		fmt.Println("user_id is missing in parameters")
		http.Error(w, "Missing user_id parameter", http.StatusBadRequest)
		return
	}

	var favoriteData map[string]string
	err := json.NewDecoder(r.Body).Decode(&favoriteData)
	if err != nil {
		fmt.Println("Error decoding request body:", err)
		http.Error(w, "Bad Request", http.StatusBadRequest)
		return
	}

	productID, exists := favoriteData["product_id"]
	if !exists {
		fmt.Println("product_id is missing in request body")
		http.Error(w, "Missing product_id parameter", http.StatusBadRequest)
		return
	}

	// Prepare the request body
	requestBody := map[string]string{"product_id": productID}
	requestJSON, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Println("Error encoding request body:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Send a POST request to the specified endpoint
	resp, err := http.Post(fmt.Sprintf("http://localhost:5000/users/%s/favorites/add", userID), "application/json", bytes.NewBuffer(requestJSON))
	if err != nil {
		fmt.Println("Error sending POST request:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	// Check the response status code
	if resp.StatusCode == http.StatusOK || resp.StatusCode == http.StatusCreated {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "Product with ID %s added to favorites for user ID: %s", productID, userID)
	} else {
		fmt.Println("Error adding product to favorites. Status Code:", resp.StatusCode)
		http.Error(w, "Error adding product to favorites", resp.StatusCode)
		return
	}

}

func SeeFavorites(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	userID, ok := vars["user_id"]

	if !ok {
		fmt.Println("user_id is missing in parameters")
		http.Error(w, "Missing user_id parameter", http.StatusBadRequest)
		return
	}

	resp, err := http.Get(fmt.Sprintf("http://localhost:5000/users/%s/favorites", userID))
	if err != nil {
		fmt.Println("Error sending GET request:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	// Read the response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading response body:", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Set the response headers and write the response body to the client
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(resp.StatusCode)
	w.Write(body)

}

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/add_product", CreateProduct)
	r.HandleFunc("/delete_product/{id}", DeleteProduct)
	r.HandleFunc("/search_products", SearchProductByName)
	r.HandleFunc("/search_all_products", SearchAllProducts)
	r.HandleFunc("/users/{user_id}/favorites/add", AddToFavorites)
	r.HandleFunc("/users/{user_id}/favorites", SeeFavorites)

	err := http.ListenAndServe(":8000", r)
	log.Fatal(err)
}
