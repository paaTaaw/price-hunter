export type Product = {
  id: string;
  name: string;
  brand: string;
  category: string;

  price: number;
  oldPrice?: number;

  currency: string;

  store: string;
  rating: number;
  reviews: number;

  image: string;
  url: string;

  discount?: number;

  inStock: boolean;

  updatedAt: string;
};

export const products: Product[] = [
  {
    id: "iphone-15-128",
    name: "Apple iPhone 15 128GB",
    brand: "Apple",
    category: "Phones",

    price: 69999,
    oldPrice: 79999,

    currency: "NPR",

    store: "Price Hunter Store",
    rating: 4.7,
    reviews: 128,

    image:
      "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd",

    url: "#",

    discount: 13,

    inStock: true,

    updatedAt: "Just now",
  },

  {
    id: "macbook-air-m2",
    name: "Apple MacBook Air M2",
    brand: "Apple",
    category: "Laptops",

    price: 119999,
    oldPrice: 139999,

    currency: "NPR",

    store: "Price Hunter Store",
    rating: 4.8,
    reviews: 94,

    image:
    "https://images.unsplash.com/photo-1496181133206-80ce9b88a853",

    url: "#",

    discount: 14,

    inStock: true,

    updatedAt: "Just now",
  },

  {
    id: "sony-wh1000xm5",
    name: "Sony WH-1000XM5 Wireless Headphones",
    brand: "Sony",
    category: "Headphones",

    price: 32999,
    oldPrice: 39999,

    currency: "NPR",

    store: "Price Hunter Store",
    rating: 4.6,
    reviews: 76,

    image:
      "https://images.unsplash.com/photo-1546435770-a3e426bf472b",

    url: "#",

    discount: 18,

    inStock: true,

    updatedAt: "Just now",
  },

  {
    id: "gaming-laptop",
    name: "ASUS ROG Gaming Laptop",
    brand: "ASUS",
    category: "Gaming",

    price: 159999,
    oldPrice: 179999,

    currency: "NPR",

    store: "Price Hunter Store",
    rating: 4.5,
    reviews: 51,

    image:
      "https://images.unsplash.com/photo-1603302576837-37561b2e2302",

    url: "#",

    discount: 11,

    inStock: true,

    updatedAt: "Just now",
  },
];