"use client";
import { useToast } from "@/hooks/use-toast";

import React from "react";

function SignOutLink() {
  const { toast } = useToast();
  const handleLogout = () => {
    toast({ description: "You have been signed out." });
  };
  return (
    <>
      <button className="w-full text-left " onClick={handleLogout}>
        Logout
      </button>
    </>
  );
}

export default SignOutLink;
