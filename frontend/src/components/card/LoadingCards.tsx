import React from "react";
import { Skeleton } from "../ui/skeleton";

export function SkeletonCard() {
  return (
    <div className="relative h-[300px] mb-2 overflow-hidden rounded-md">
      <div>
        <Skeleton className="h-[200px] w-[250px] rounded-md" />
      </div>
      <Skeleton className="h-4 mt-4 w-3/4" />
      <Skeleton className="h-4 mt-2 w-1/2" />
      <Skeleton className="h-4 mt-2 w-1/4" />
    </div>
  );
}

function LoadingCards() {
  return (
    <div className="mt-4 gap-8 grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <SkeletonCard />
      <SkeletonCard />
      <SkeletonCard />
      <SkeletonCard />
      <SkeletonCard />
      <SkeletonCard />
      <SkeletonCard />
      <SkeletonCard />
      <SkeletonCard />
    </div>
  );
}

export default LoadingCards;
