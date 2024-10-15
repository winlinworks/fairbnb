import React from "react";
import { Button } from "@/components/ui/button";
import CategoriesList from "@/components/home/CategoriesList";
import PropertgiesContainer from "@/components/home/PropertyContainer";

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
      {/* <PropertgiesContainer
        category={searchParams?.category}
        search={searchParams.search}
      /> */}
    </section>
  );
}

export default HomePage;
