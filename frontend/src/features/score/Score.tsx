import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export const Score: React.FC = () => {
  return (
    <div className="w-full">
      <Tabs defaultValue="overall">
        <TabsList className="bg-transparent flex flex-wrap w-full gap-2 h-auto mb-6">
          <TabsTrigger
            value="overall"
            className="px-6 text-lg data-[state=inactive]:bg-transparent data-[state=active]:bg-muted gap-2"
          >
            <span>Overall</span>
            <Badge className="rounded-full">240</Badge>
          </TabsTrigger>
          <TabsTrigger
            value="writing"
            className="px-6 text-lg data-[state=inactive]:bg-transparent data-[state=active]:bg-muted gap-2"
          >
            <span>Writing</span>
            <Badge className="rounded-full">60</Badge>
          </TabsTrigger>
          <TabsTrigger
            value="speaking"
            className="px-6 text-lg data-[state=inactive]:bg-transparent data-[state=active]:bg-muted gap-2"
          >
            <span>Speaking</span>
            <Badge className="rounded-full">60</Badge>
          </TabsTrigger>
          <TabsTrigger
            value="reading"
            className="px-6 text-lg data-[state=inactive]:bg-transparent data-[state=active]:bg-muted gap-2"
          >
            <span>Reading</span>
            <Badge className="rounded-full">60</Badge>
          </TabsTrigger>
          <TabsTrigger
            value="listening"
            className="px-6 text-lg data-[state=inactive]:bg-transparent data-[state=active]:bg-muted gap-2"
          >
            <span>Listening</span>
            <Badge className="rounded-full">60</Badge>
          </TabsTrigger>
        </TabsList>
        <TabsContent value="overall">
          <div className="bg-muted p-4 rounded-lg">
            <h1>Overall</h1>
          </div>
        </TabsContent>
        <TabsContent value="writing">
          <h1>Writing</h1>
        </TabsContent>
        <TabsContent value="speaking">
          <h1>Speaking</h1>
        </TabsContent>
        <TabsContent value="reading">
          <h1>Reading</h1>
        </TabsContent>
        <TabsContent value="listening">
          <h1>Listening</h1>
        </TabsContent>
      </Tabs>
    </div>
  );
};
