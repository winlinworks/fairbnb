import React from "react";
import { Button } from "@/components/ui/button";
import CategoriesList from "@/components/home/CategoriesList";
import PropertgiesContainer from "@/components/home/PropertiesContainer";
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
      <PropertgiesContainer
        category={searchParams?.category}
        search={searchParams.search}
      />
    </section>
  );
}

export default HomePage;
