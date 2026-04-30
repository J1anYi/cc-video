import { useState, useEffect } from 'react';
import { marketplaceApi, MarketplaceListing, ListingFilters } from '../../api/marketplace';

export default function ContentMarketplace() {
  const [listings, setListings] = useState<MarketplaceListing[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [pricingType, setPricingType] = useState<string>('');
  const [selectedListing, setSelectedListing] = useState<MarketplaceListing | null>(null);
  const [showPurchaseModal, setShowPurchaseModal] = useState(false);

  useEffect(() => {
    loadListings();
  }, [search, pricingType]);

  const loadListings = async () => {
    setLoading(true);
    try {
      const filters: ListingFilters = {};
      if (search) filters.search = search;
      if (pricingType) filters.pricing_type = pricingType;
      const response = await marketplaceApi.getListings(filters);
      setListings(response.listings);
    } catch (error) {
      console.error('Failed to load listings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = async (tierId?: number) => {
    if (!selectedListing) return;
    try {
      const result = await marketplaceApi.purchaseLicense(selectedListing.id, { tier_id: tierId });
      alert('Purchase successful! License ID: ' + result.license_id);
      setShowPurchaseModal(false);
      setSelectedListing(null);
    } catch (error) {
      console.error('Purchase failed:', error);
      alert('Purchase failed. Please try again.');
    }
  };

  const formatPrice = (price: number, currency: string) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: currency }).format(price);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Content Marketplace</h1>
      <div className="flex gap-4 mb-6">
        <input type="text" placeholder="Search listings..." value={search} onChange={(e) => setSearch(e.target.value)} className="flex-1 px-4 py-2 border rounded-lg" />
        <select value={pricingType} onChange={(e) => setPricingType(e.target.value)} className="px-4 py-2 border rounded-lg">
          <option value="">All Pricing Types</option>
          <option value="per_view">Per View</option>
          <option value="subscription">Subscription</option>
          <option value="purchase">Purchase</option>
        </select>
      </div>
      {loading ? (
        <div className="text-center py-8">Loading...</div>
      ) : listings.length === 0 ? (
        <div className="text-center py-8 text-gray-500">No listings found</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {listings.map((listing) => (
            <div key={listing.id} className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer hover:shadow-lg" onClick={() => setSelectedListing(listing)}>
              <div className="p-4">
                <h3 className="text-lg font-semibold mb-2">{listing.title}</h3>
                {listing.description && <p className="text-gray-600 text-sm mb-3">{listing.description}</p>}
                <div className="flex items-center justify-between">
                  <span className="text-lg font-bold text-blue-600">{formatPrice(listing.base_price, listing.currency)}</span>
                  <span className="text-xs bg-gray-100 px-2 py-1 rounded">{listing.pricing_type}</span>
                </div>
                <div className="mt-2 text-xs text-gray-500">{listing.purchase_count} purchases | {listing.view_count} views</div>
              </div>
            </div>
          ))}
        </div>
      )}
      {selectedListing && !showPurchaseModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto p-6">
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-2xl font-bold">{selectedListing.title}</h2>
              <button onClick={() => setSelectedListing(null)} className="text-gray-500">X</button>
            </div>
            {selectedListing.description && <p className="text-gray-600 mb-4">{selectedListing.description}</p>}
            <div className="mb-4">
              <span className="text-2xl font-bold text-blue-600">{formatPrice(selectedListing.base_price, selectedListing.currency)}</span>
            </div>
            <div className="flex gap-2">
              <button onClick={() => setShowPurchaseModal(true)} className="flex-1 bg-blue-600 text-white py-2 rounded-lg">Purchase</button>
              <button onClick={() => setSelectedListing(null)} className="flex-1 border py-2 rounded-lg">Cancel</button>
            </div>
          </div>
        </div>
      )}
      {selectedListing && showPurchaseModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h2 className="text-xl font-bold mb-4">Confirm Purchase</h2>
            <p className="mb-4">Purchase {selectedListing.title} for {formatPrice(selectedListing.base_price, selectedListing.currency)}</p>
            <div className="flex gap-2">
              <button onClick={() => handlePurchase()} className="flex-1 bg-blue-600 text-white py-2 rounded-lg">Confirm</button>
              <button onClick={() => setShowPurchaseModal(false)} className="flex-1 border py-2 rounded-lg">Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
