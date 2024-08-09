import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Textarea } from "@/components/ui/textarea";
import { useChat } from "@/contexts/chat";
import { ChatMessage, ChatSender, ChatType } from "@/models/chat";
import { zodResolver } from "@hookform/resolvers/zod";
import React from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

const BoxSchema = z.object({
  answer: z
    .string()
    .min(10, {
      message: "Bio must be at least 10 characters.",
    })
    .max(160, {
      message: "Bio must not be longer than 30 characters.",
    }),
});

export const MessageBox: React.FC = () => {
  const { sendMessage } = useChat();
  const form = useForm<z.infer<typeof BoxSchema>>({
    resolver: zodResolver(BoxSchema),
  });

  const onSubmit = (data: z.infer<typeof BoxSchema>) => {
    const chatMessage: ChatMessage = {
      type: ChatType.TEXT,
      content: data.answer,
      created: new Date(),
      is_modified: false,
      sender: ChatSender.USER,
    };
    sendMessage(chatMessage);
  };

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="w-full flex flex-col items-end gap-4"
      >
        <FormField
          control={form.control}
          name="answer"
          render={({ field }) => (
            <FormItem className="w-full">
              <FormControl>
                <Textarea
                  placeholder="Write your answer here!"
                  className="w-full resize-none"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Send</Button>
      </form>
    </Form>
  );
};
