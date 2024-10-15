import React from "react";
import { Skeleton } from "../ui/skeleton";

export function SkeletonCard() {
  return (
    <div>
      <Skeleton className="h-[300xp] rounded-md" />
      <Skeleton className="h-4 mt-4 w-3/4" />
      <Skeleton className="h-4 mt-4 w-1/2" />
    </div>
  );
}

function LoadingCards() {
  return (
    <section className="mt-4 gap-8 grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <SkeletonCard />
      <SkeletonCard />
      <SkeletonCard />
      <SkeletonCard />
    </section>
  );
}

export default LoadingCards;
