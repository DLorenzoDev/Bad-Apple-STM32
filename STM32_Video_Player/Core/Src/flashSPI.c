/*
 * flashSPI.c
 *
 *  Created on: Aug 30, 2025
 *      Author: Daniel
 */

#include "flashSPI.h"

extern SPI_HandleTypeDef hspi1;
#define FLASH_CS_PIN GPIO_PIN_4
#define FLASH_CS_PORT GPIOA

static void FLASH_CS_LOW() { HAL_GPIO_WritePin(FLASH_CS_PORT, FLASH_CS_PIN, GPIO_PIN_RESET); }
static void FLASH_CS_HIGH(){ HAL_GPIO_WritePin(FLASH_CS_PORT, FLASH_CS_PIN, GPIO_PIN_SET); }

static void SPI_FLASH_WriteEnable() {
    uint8_t cmd = 0x06;
    FLASH_CS_LOW();
    HAL_SPI_Transmit(&hspi1, &cmd, 1, HAL_MAX_DELAY);
    FLASH_CS_HIGH();
}

void SPI_FLASH_Init(void) { /* nada especial para W25Q */ }

void SPI_FLASH_EraseSector(uint32_t sector_addr) {
    SPI_FLASH_WriteEnable();
    uint8_t cmd[4] = {0x20, (sector_addr>>16)&0xFF, (sector_addr>>8)&0xFF, sector_addr&0xFF};
    FLASH_CS_LOW();
    HAL_SPI_Transmit(&hspi1, cmd, 4, HAL_MAX_DELAY);
    FLASH_CS_HIGH();
    HAL_Delay(50); // esperar borrado
}

void SPI_FLASH_Write(uint32_t addr, uint8_t* buf, uint32_t len) {
    while(len) {
        SPI_FLASH_WriteEnable();
        uint16_t chunk = (len > 256) ? 256 : len; // Page program max 256 bytes
        uint8_t cmd[4] = {0x02, (addr>>16)&0xFF, (addr>>8)&0xFF, addr&0xFF};
        FLASH_CS_LOW();
        HAL_SPI_Transmit(&hspi1, cmd, 4, HAL_MAX_DELAY);
        HAL_SPI_Transmit(&hspi1, buf, chunk, HAL_MAX_DELAY);
        FLASH_CS_HIGH();
        HAL_Delay(1);
        addr += chunk;
        buf += chunk;
        len -= chunk;
    }
}


void SPI_FLASH_Read(uint32_t addr, uint8_t* buf, uint32_t len) {
    uint8_t cmd[4] = {0x03, (addr>>16)&0xFF, (addr>>8)&0xFF, addr&0xFF};
    FLASH_CS_LOW();
    HAL_SPI_Transmit(&hspi1, cmd, 4, HAL_MAX_DELAY);
    HAL_SPI_Receive(&hspi1, buf, len, HAL_MAX_DELAY);
    FLASH_CS_HIGH();
}

void SPI_FLASH_WaitForReady(void) {
    uint8_t cmd = 0x05, status;
    do {
        FLASH_CS_LOW();
        HAL_SPI_Transmit(&hspi1, &cmd, 1, HAL_MAX_DELAY);
        HAL_SPI_Receive(&hspi1, &status, 1, HAL_MAX_DELAY);
        FLASH_CS_HIGH();
    } while (status & 0x01);
}

