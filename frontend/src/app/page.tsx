import React from "react";
import { Button } from "@/components/ui/button";
import CategoriesList from "@/components/home/CategoriesList";
import PropertiesContainer from "@/components/home/PropertiesContainer";
import LoadingCards from "@/components/card/LoadingCards";

function HomePage({
  searchParams,
}: {
  searchParams: { category?: string; search?: string };
}) {
  return (
    <section>
      <CategoriesList
        category={searchParams?.category}
        search={searchParams.search}
      />
      {/* <LoadingCards /> */}
      <PropertiesContainer
        category={searchParams?.category}
        search={searchParams.search}
      />
    </section>
  );
}

export default HomePage;
