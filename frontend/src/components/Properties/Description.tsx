// "use client";
// import { useState } from "react";
// import { Button } from "@/components/ui/button";
// import Title from "./Title";

// function Description({ description }: { description: string }) {
//   const [isFullDescriptionShown, setIsFullDescriptionShown] = useState(false);
//   const words = description.split(" ");
//   const isLongDescription = words.length > 50;

//   const toggleDescription = () => {
//     setIsFullDescriptionShown(!isFullDescriptionShown);
//   };

//   const displayedDescription =
//     isLongDescription && !isFullDescriptionShown
//       ? words.splice(0, 50).join(" ") + "..."
//       : description;

//   return (
//     <article className="mt-4">
//       <Title text="Description" />
//       <p className="text-muted-foreground font-light leading-loose">
//         {displayedDescription}
//       </p>
//       {isLongDescription && (
//         <Button
//           variant="link"
//           className="text-primary-500"
//           onClick={toggleDescription}
//         >
//           {isFullDescriptionShown ? "Show less" : "Show more"}
//         </Button>
//       )}
//     </article>
//   );
// }

// export default Description;
