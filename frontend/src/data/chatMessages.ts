import { MaybeRefOrGetter, toValue } from 'vue'
import { useDoc, useList } from 'frappe-ui/src/data-fetching'
import { UseListOptions } from 'frappe-ui/src/data-fetching/useList/types'
import { GPChatMessage } from '@/types/doctypes'
import { useUser } from './users'

export interface ChatMessage extends GPChatMessage {
  project_title?: string
  user_full_name?: string
  user_image?: string
  owner_full_name?: string
  owner_user_image?: string
}

export type UseChatMessagesOptions = Pick<
  UseListOptions<ChatMessage>,
  'cacheKey' | 'filters' | 'limit' | 'orderBy' | 'immediate'
>

export function useChatMessages(options: UseChatMessagesOptions) {
  const messages = useList<ChatMessage>({
    doctype: 'GP Chat Message',
    fields: [
      'name',
      'content',
      'project',
      'pod',
      'message_type',
      'edited_at',
      'deleted_at',
      'creation',
      'modified',
      'owner',
      'reactions',
      'tags',
    ],
    cacheKey: options.cacheKey ? ['ChatMessages', options.cacheKey] : undefined,
    filters: options.filters,
    limit: options.limit || 50,
    orderBy: options.orderBy || 'creation asc',
    immediate: options.immediate ?? true,
    transform(data) {
      return data.map((message) => {
        const ownerUser = useUser(message.owner)
        return {
          ...message,
          owner_full_name: ownerUser.full_name,
          owner_user_image: ownerUser.user_image,
          user_full_name: ownerUser.full_name,
          user_image: ownerUser.user_image,
        }
      })
    },
  })
  return messages
}

let chatMessagesCache: Record<string, ReturnType<typeof useDoc>> = {}

export function useChatMessage(messageId: MaybeRefOrGetter<string>) {
  interface ChatMessageMethods {
    edit_message: (content: string) => string
  }

  function getCacheKey() {
    return toValue(messageId)
  }

  let cacheKey = getCacheKey()
  if (!chatMessagesCache[cacheKey]) {
    chatMessagesCache[cacheKey] = useDoc<GPChatMessage, ChatMessageMethods>({
      doctype: 'GP Chat Message',
      name: () => toValue(messageId),
      methods: {
        edit_message: 'edit_message',
      },
    })
  }

  return chatMessagesCache[cacheKey]
}
