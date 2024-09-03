import React from "react";
import { Button } from "@/components/ui/button";

function HomePage() {
  return (
    <div>
      <h1 className="text-3xl ">Home Page</h1>
      <Button variant="destructive" size="lg" className="text-xl bg-slate-300">
        Try me
      </Button>
    </div>
  );
}

export default HomePage;
