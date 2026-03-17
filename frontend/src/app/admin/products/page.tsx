"use client";

import { useEffect, useState } from "react";
import { Package, Search, RefreshCw } from "lucide-react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  stock: number;
}

function StockBadge({ stock }: { stock: number }) {
  if (stock === 0) {
    return (
      <span className="text-xs font-medium px-2.5 py-0.5 rounded-full bg-red-400/10 text-red-400 border border-red-400/20">
        Out of Stock
      </span>
    );
  }
  if (stock <= 20) {
    return (
      <span className="text-xs font-medium px-2.5 py-0.5 rounded-full bg-orange-400/10 text-orange-400 border border-orange-400/20">
        Low Stock ({stock})
      </span>
    );
  }
  return (
    <span className="text-xs font-medium px-2.5 py-0.5 rounded-full bg-emerald-400/10 text-emerald-400 border border-emerald-400/20">
      In Stock ({stock})
    </span>
  );
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  const fetchProducts = (q = "") => {
    setLoading(true);
    fetch(`${API_BASE}/api/v1/products?q=${encodeURIComponent(q)}&limit=50`)
      .then((r) => r.json())
      .then((d) => setProducts(d.products || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchProducts(search);
  };

  const categories = Array.from(new Set(products.map((p) => p.category)));

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Package className="h-6 w-6 text-indigo-400" />
            Product Catalog
          </h1>
          <p className="text-gray-400 text-sm mt-1">
            {products.length} products in catalog
          </p>
        </div>
        <button
          onClick={() => fetchProducts(search)}
          className="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors border border-white/10 rounded-lg px-3 py-2 hover:border-white/20"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </div>

      {/* Search & Filters */}
      <div className="mb-6 flex gap-4 items-center">
        <form onSubmit={handleSearch} className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
          <input
            id="product-search"
            type="text"
            placeholder="Search products by name, description or category..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500/50 transition-colors"
          />
        </form>
        <button
          type="submit"
          form="product-search"
          onClick={handleSearch}
          className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-sm rounded-lg transition-colors"
        >
          Search
        </button>
      </div>

      {/* Category pills */}
      {categories.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-6">
          <button
            onClick={() => { setSearch(""); fetchProducts(""); }}
            className="text-xs px-3 py-1 rounded-full border border-white/10 text-gray-400 hover:text-white hover:border-white/20 transition-colors"
          >
            All
          </button>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => { setSearch(cat); fetchProducts(cat); }}
              className="text-xs px-3 py-1 rounded-full border border-white/10 text-gray-400 hover:text-white hover:border-white/20 transition-colors"
            >
              {cat}
            </button>
          ))}
        </div>
      )}

      {/* Table */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="h-8 w-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : products.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <Package className="h-12 w-12 mx-auto mb-4 opacity-30" />
          <p>No products found.</p>
        </div>
      ) : (
        <div className="rounded-xl border border-white/10 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/10 bg-white/[0.02]">
                <th className="text-left text-gray-400 font-medium py-3 px-5">Product</th>
                <th className="text-left text-gray-400 font-medium py-3 px-5">Category</th>
                <th className="text-right text-gray-400 font-medium py-3 px-5">Price</th>
                <th className="text-left text-gray-400 font-medium py-3 px-5">Stock</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product, i) => (
                <tr
                  key={product.id}
                  className={`border-b border-white/5 hover:bg-white/[0.03] transition-colors ${
                    i === products.length - 1 ? "border-0" : ""
                  }`}
                >
                  <td className="py-4 px-5">
                    <p className="text-white font-medium">{product.name}</p>
                    <p className="text-gray-500 text-xs mt-0.5 line-clamp-1">
                      {product.description}
                    </p>
                  </td>
                  <td className="py-4 px-5">
                    <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-400/10 text-indigo-400 border border-indigo-400/20">
                      {product.category}
                    </span>
                  </td>
                  <td className="py-4 px-5 text-right">
                    <span className="text-white font-medium">
                      ₹{product.price.toLocaleString("en-IN")}
                    </span>
                  </td>
                  <td className="py-4 px-5">
                    <StockBadge stock={product.stock} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
