/*
Project 1: Send and receive a simple message: Hello Server!
 *
 */

#include <stdio.h>
#include <string.h>

#include "lwip/sockets.h"
#include "netif/xadapter.h"
#include "lwipopts.h"
#include "xil_printf.h"
#include "FreeRTOS.h"
#include "task.h"

#define THREAD_STACKSIZE 1024
/*
 * Max number of telnet connections that this application can serve.
 * The existing implementation does not support closing of an existing telnet.
 * Once a telnet connection is made, it stays for ever.
 */
#define MAX_CONNECTIONS 100
int new_sd[MAX_CONNECTIONS];
int connection_index;

u16_t echo_port = 7;

void print_echo_app_header()
{
    xil_printf("%20s %6d %s\r\n", "echo server",
                        echo_port,
                        "$ telnet <board_ip> 7");

}

/* thread spawned for each connection */
void process_echo_request(void *p)
{
    int sd = *(int *)p;
    int RECV_BUF_SIZE = 1024;
    int SEND_BUF_SIZE = 1024;
    char recv_buf[RECV_BUF_SIZE];
    int n, nwrote;
    const char *suffix = " - Server response"; // Text to append
    char send_buf[SEND_BUF_SIZE];         // Buffer for modified message

    while (1) {
        /* read a max of RECV_BUF_SIZE bytes from socket */
        if ((n = read(sd, recv_buf, RECV_BUF_SIZE)) < 0) {
            xil_printf("%s: error reading from socket %d, closing socket\r\n", __FUNCTION__, sd);
            break;
        }

        /* break if the recved message = "quit" */
        if (!strncmp(recv_buf, "quit", 4))
            break;

        /* break if client closed connection */
        if (n <= 0)
            break;

        /* Add null terminator to received buffer */
        recv_buf[n] = '\0';

        /* Append the suffix */
        snprintf(send_buf, sizeof(send_buf), "%s%s", recv_buf, suffix);

        /* handle request */
        if ((nwrote = write(sd, send_buf, strlen(send_buf))) < 0) {
            xil_printf("%s: ERROR responding to client echo request. received = %d, written = %d\r\n",
                    __FUNCTION__, n, nwrote);
            xil_printf("Closing socket %d\r\n", sd);
            break;
        }
    }

    /* close connection */
    close(sd);
    vTaskDelete(NULL);
}


void echo_application_thread()
{
	int sock;
	int size;
#if LWIP_IPV6==0
	struct sockaddr_in address, remote;

	memset(&address, 0, sizeof(address));

	if ((sock = lwip_socket(AF_INET, SOCK_STREAM, 0)) < 0)
		return;

	address.sin_family = AF_INET;
	address.sin_port = htons(echo_port);
	address.sin_addr.s_addr = INADDR_ANY;
#else
	struct sockaddr_in6 address, remote;

	memset(&address, 0, sizeof(address));

	address.sin6_len = sizeof(address);
	address.sin6_family = AF_INET6;
	address.sin6_port = htons(echo_port);

	memset(&(address.sin6_addr), 0, sizeof(address.sin6_addr));

	if ((sock = lwip_socket(AF_INET6, SOCK_STREAM, 0)) < 0)
		return;
#endif

	if (lwip_bind(sock, (struct sockaddr *)&address, sizeof (address)) < 0)
		return;

	lwip_listen(sock, 0);

	size = sizeof(remote);

	while (1) {
		if ((new_sd[connection_index] = lwip_accept(sock, (struct sockaddr *)&remote, (socklen_t *)&size)) > 0) {
			sys_thread_new("echos", process_echo_request,
				(void*)&(new_sd[connection_index]),
				THREAD_STACKSIZE,
				DEFAULT_THREAD_PRIO);
			if (++connection_index>= MAX_CONNECTIONS) {
				break;
			}
		}
	}
	xil_printf("Maximum number of connections reached, No further connections will be accepted\r\n");
	vTaskSuspend(NULL);
}
