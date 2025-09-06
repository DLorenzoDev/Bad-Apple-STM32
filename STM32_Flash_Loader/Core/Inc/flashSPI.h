/*
 * flashSPI.h
 *
 *  Created on: Aug 30, 2025
 *      Author: Daniel
 */

#ifndef INC_FLASHSPI_H_
#define INC_FLASHSPI_H_

#include "stm32f4xx_hal.h"

#define SPI_FLASH_SECTOR_SIZE 4096

void SPI_FLASH_Init(void);
void SPI_FLASH_EraseSector(uint32_t sector_addr);
void SPI_FLASH_Write(uint32_t addr, uint8_t* buf, uint32_t len);
void SPI_FLASH_Read(uint32_t addr, uint8_t* buf, uint32_t len);

#endif /* INC_FLASHSPI_H_ */
