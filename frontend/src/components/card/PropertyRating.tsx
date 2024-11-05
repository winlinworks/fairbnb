import React from "react";
import { FaStar } from "react-icons/fa";

function PropertyRating({
  propertyId,
  inPage,
}: {
  propertyId: string;
  inPage: boolean;
}) {
  const rating = 4.6;
  const count = 106;

  const className = `flex gap-1 items=center ${inPage ? "text-md" : "text-xs"}`;
  const countText = count > 1 ? "reviews" : "review";
  const countValue = `(${count}) ${inPage ? countText : ""}`;

  return (
    <span className={className}>
      <FaStar className="w-3 h-3" /> {rating} {countValue}
    </span>
  );
}

export default PropertyRating;
