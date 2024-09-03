import React from "react";
import Link from "next/link";
import { TbTent } from "react-icons/tb";
import { Button } from "../button";

function Logo() {
  return (
    <Button size="icon" asChild>
      <Link href="/">
        <TbTent className="w-8 h-8" />
      </Link>
    </Button>
  );
}

export default Logo;
